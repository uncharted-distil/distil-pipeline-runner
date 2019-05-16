"""
   Copyright © 2019 Uncharted Software Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import time
import os
from typing import List, Dict, Set, Any, Optional
from concurrent import futures
import pprint
import logging

import importlib
import pipeline_pb2
import pipeline_pb2_grpc
import value_pb2
import value_pb2_grpc

from d3m import runtime
from d3m import container
from d3m.metadata import base as metadata_base
from d3m.metadata import pipeline as metadata_pipeline
from ta3ta2_api import utils

import frozendict

_logger = logging.getLogger(__name__)

_input_table: List[container.Dataset] = []
_output_table: Dict[int, Dict[str, Any]] = {}

# cache of instantiated primitives - loading can be a slow process so we want to
# do it once for the life time of the runner
_primitive_cache: Dict[str, Any] = {}

def _resolve_output(dataref: str) -> Any:
    dataref_parts = dataref.split(".")
    if dataref_parts[0] == 'inputs':
        # for pipeline inputs references pull from the inputs table
        return _input_table[int(dataref_parts[1])]
    if dataref_parts[0] == 'steps':
        # for references to other pipeline steps, pull from the outputs table which is
        # addressed by step index and output name
        return _output_table[int(dataref_parts[1])][dataref_parts[2]]
    return []


def _get_input(primitive_step: pipeline_pb2.PrimitivePipelineDescriptionStep) -> Dict[str, Any]:
    # get the actual input data container (ie. Dataset, Dataframe) using the step's data references
    inputs: Dict[str, Any] = {}
    for arg_name in primitive_step.arguments:
        arg_value = primitive_step.arguments[arg_name]
        inputs[arg_name] = _resolve_output(arg_value.container.data)
    return inputs


def _get_hyperparameters(primitive_step: pipeline_pb2.PrimitivePipelineDescriptionStep,
                         primitive_class: frozendict.FrozenOrderedDict) -> Dict[str, Any]:
    # parse out hyperparameter structures and initialize with defaults
    primitive_hyperparams_class = \
        primitive_class.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
    hyperparams = primitive_hyperparams_class.defaults()
    new_hyperparams = dict(hyperparams)

    # iterate over entries and add values to hyperparameter struct
    for hyperparam_key, hyperparam_value in primitive_step.hyperparams.items():
        if hyperparam_value.WhichOneof('argument') == 'value':
            parsed_param = _get_raw_hyperparameter(hyperparam_value.value.data.raw)
            new_hyperparams[hyperparam_key] = parsed_param

    return new_hyperparams


def _get_list_hyperparameter(list: value_pb2.ValueList) -> Any:
    result_list = []
    for value in list.items:
        which_value = value.WhichOneof('raw')
        if which_value == 'list':
            result_list.append(_get_list_hyperparameter(value.list))
        elif which_value == 'dict':
            result_list.append(_get_dict_hyperparameter(value.dict))
        else:
            result_list.append(_get_raw_hyperparameter(value))

    return result_list


def _get_dict_hyperparameter(dict: value_pb2.ValueDict) -> Any:
    result_dict: Dict[str, Any] = {}
    for key, value in dict.items.items():
        which_value = value.WhichOneof('raw')
        if which_value == 'list':
            result_dict[key] = _get_list_hyperparameter(value.list)
        elif which_value == 'dict':
            result_dict[key] = _get_dict_hyperparameter(value.dict)
        else:
            result_dict[key] = _get_raw_hyperparameter(value)

    return result_dict


def _get_raw_hyperparameter(value: value_pb2.ValueRaw) -> Any:
    which_value = value.WhichOneof('raw')
    if which_value == 'null':
        return value.null
    if which_value == 'double':
        return value.double
    if which_value == 'int64':
        return value.int64
    if which_value == 'bool':
        return value.bool
    if which_value == 'string':
        return value.string
    if which_value == 'bytes':
        return value.bytes
    if which_value == 'list':
        return _get_list_hyperparameter(value.list)
    if which_value == 'dict':
        return _get_dict_hyperparameter(value.dict)

    return None


def _get_static_resources(primitive_class: frozendict.FrozenOrderedDict,
                          static_res_path: Optional[str]) -> Optional[Dict[str, str]]:
    # create a table of static resource paths for this primitive if specified
    for installation in primitive_class.metadata.query()['installation']:
        if installation['type'] is 'TGZ':
            volumes = {}

            if static_res_path:
                if os.path.isdir(os.path.join(static_res_path, installation['file_digest'])):
                    volumes[installation['key']] = os.path.join(static_res_path,  installation['file_digest'])
                else:
                    volumes[installation['key']] = os.path.join(static_res_path, installation['key'])
            else:
                if os.path.isdir(installation['file_digest']):
                    volumes[installation['key']] = os.path.join(installation['file_digest'])
                else:
                    volumes[installation['key']] = installation['key']

            return volumes
    return None


def _load_pipeline(filename: str) -> pipeline_pb2.PipelineDescription:
    f = open(filename, "rb")
    pipeline = pipeline_pb2.PipelineDescription()
    pipeline.ParseFromString(f.read())
    f.close()
    return pipeline


def _create_child_lookup(pipeline: pipeline_pb2.PipelineDescription) -> Dict[int, List[int]]:
    # create a dict that provides the children for a given step.  The key is the step index of the
    # parent, the value returned is a list of child step indices.
    node_children: Dict[int, List[int]] = {}
    for step_idx, step in enumerate(pipeline.steps):
        primitive_step = step.primitive
        for arg_name in primitive_step.arguments:
            arg_value = primitive_step.arguments[arg_name]
            ref_parts = arg_value.container.data.split(".")
            # references that point to input datasets should be skipped
            if ref_parts[0] != "inputs":
                parent_idx = ref_parts[1]
                if parent_idx not in node_children:
                    parent_children: List[int] = []
                    node_children[int(parent_idx)] = parent_children
                node_children[int(parent_idx)].append(step_idx)
    return node_children


def _traverse_step(step_idx: int,
                   child_lookup: Dict[int, List[int]],
                   visited: Set[int],
                   processed: List[int]) -> None:

    visited.add(step_idx)
    if step_idx in child_lookup:
        children = child_lookup[step_idx]
        for child_idx in children:
            if child_idx not in visited:
                _traverse_step(child_idx, child_lookup, visited, processed)
    processed.append(step_idx)
    return


def _sort_pipeline_steps(pipeline: pipeline_pb2.PipelineDescription) -> List[pipeline_pb2.PipelineDescriptionStep]:
    child_lookup = _create_child_lookup(pipeline)

    # find the graph source nodes - these are primitive steps that only take dataset references as
    # inputs
    sources: List[int] = []
    visited: Set[int] = set()
    for step_idx, step in enumerate(pipeline.steps):
        primitive_step = step.primitive
        source = True
        for arg_name in primitive_step.arguments:
            ref_parts = primitive_step.arguments[arg_name].container.data.split(".")
            if ref_parts[0] != 'inputs':
                source = False
                break
        if source:
            sources.append(step_idx)

    # starting at the source nodes, do a post-order traversal and store the processed nodes in a list
    processed: List[int] = []
    for source_idx in sources:
        _traverse_step(source_idx, child_lookup,  visited, processed)

    # reverse the processed list to get topologically sorted steps
    # store the original index so that we can get back to the pipeline specification
    # order
    ordered_steps = [(idx, pipeline.steps[idx]) for idx in reversed(processed)]

    return ordered_steps

def _load_inputs(dataset_filenames: List[str]) -> List[container.Dataset]:
    input_datasets = []
    for dataset_filename in dataset_filenames:
        input_dataset = container.Dataset.load(dataset_filename)
        input_datasets.append(input_dataset)
    return input_datasets

def execute_pipeline(pipeline: pipeline_pb2.PipelineDescription,
                     dataset_filenames: List[str],
                     static_resource_path: Optional[str] = None) -> Any:
    """
        Executes a binary protobuf pipeline against a supplied d3m dataset.

    Parameters
    ----------
    pipeline: protobuf pipeline definition
    dataset_filenames: paths to folders containing input D3M datasets

    Returns
    -------
    The result of the pipeline execution.
    """

    # transform the pipeline to the internal d3m representation
    pipeline_d3m = utils.decode_pipeline_description(pipeline, metadata_pipeline.Resolver())

    rt = runtime.Runtime(pipeline_d3m, context=metadata_base.Context.TESTING)

    # load the data
    inputs = _load_inputs(dataset_filenames)

    # call the runtime produce

    return rt.produce(inputs=inputs)
    """
    _input_table.clear()
    _output_table.clear()

    # load the input dataset and add it to the input table
    for dataset_filename in dataset_filenames:
        input_dataset = container.Dataset.load(dataset_filename)
        _input_table.append(input_dataset)

    # perform a topological sort of the pipeline DAG to get an ordering that takes
    # dependencies into account
    sorted_steps = _sort_pipeline_steps(pipeline)

    for step_idx, step in sorted_steps:
        # load the primitive class
        python_path = step.primitive.primitive.python_path
        primitive_class = None
        path, name = python_path.rsplit('.', 1)
        if python_path not in _primitive_cache.keys():
            _logger.info("Primitive " + python_path + " not cached.  Loading.")
            module = importlib.import_module(path)
            primitive_class = getattr(module, name)
            _primitive_cache[python_path] = primitive_class
        else:
            _logger.info("Using cached primitive " + python_path)
            primitive_class = _primitive_cache[python_path]

        # get the static resource table, hyperparams, and instantiate the primitive
        static_resources = _get_static_resources(primitive_class, static_resource_path)
        hyperparams = _get_hyperparameters(step.primitive, primitive_class)

        _logger.info('Executing primitive ' + path + '.' + name)
        _logger.info('Hyperparams:\n ' + pprint.pformat(hyperparams))
        _logger.info('Resources:\n ' + pprint.pformat(static_resources))

        primitive = None
        if static_resources:
            primitive = primitive_class(hyperparams=hyperparams, volumes=static_resources)
        else:
            primitive = primitive_class(hyperparams=hyperparams)

        # reflectively call each output method using the hyperparams and extracted arguments
        for output in step.primitive.outputs:
            input_data = _get_input(step.primitive)
            result = getattr(primitive, output.id)(**input_data)
            _output_table[step_idx] = {output.id: result.value}

            _logger.debug('Result\n' + str(result.value))

    # extract the final output
    output_dataref = pipeline.outputs[0].data
    return _resolve_output(output_dataref)
    """


def execute_pipeline_file(pipeline_filename: str,
                          dataset_filenames: List[str],
                          static_resource_path: str = None) -> Any:
    """
        Executes a binary protobuf pipeline against a supplied d3m dataset.

    Parameters
    ----------
    pipeline_filename: path to binary protobuf pipeline definition
    dataset_filenames: paths to folders containing input D3M datasets

    Returns
    -------
    The result of the pipeline execution.
    """

    # load the protobuf pipeline def
    pipeline = _load_pipeline(pipeline_filename)
    _logger.info('Executing pipeline: \n' + str(pipeline))
    return execute_pipeline(pipeline, dataset_filenames, static_resource_path)
