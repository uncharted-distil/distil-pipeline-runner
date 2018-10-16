#!/bin/bash

import time
import os
from typing import List, Dict, Any, Optional
from concurrent import futures

import importlib
import pipeline_pb2
import pipeline_pb2_grpc
import value_pb2
import value_pb2_grpc

from d3m import container
from d3m.metadata import base as metadata_base

import frozendict

_input_table: List[container.Dataset] = []
_output_table: List[Dict[str, Any]] = []


def _resolve_output(dataref: str) -> List[Dict[str, Any]]:
    # on inputs use the input dataset, on subsequent
    dataref_parts = dataref.split(".")
    if dataref_parts[0] == 'inputs':
        return _input_table[int(dataref_parts[1])]
    if dataref_parts[0] == 'steps':
        return _output_table[int(dataref_parts[1])][dataref_parts[2]]
    return []


def _get_input(primitive_step: pipeline_pb2.PrimitivePipelineDescriptionStep) -> List[Dict[str, Any]]:
    # get the input data reference
    inputs = primitive_step.arguments['inputs']
    dataref = inputs.container.data
    return _resolve_output(dataref)


def _get_hyperparameters(primitive_step: pipeline_pb2.PrimitivePipelineDescriptionStep,
                         primitive_class: frozendict.FrozenOrderedDict) -> Any:
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
                volumes[installation['key']] = os.path.join(static_res_path, installation['key'])
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


def execute_pipeline(pipeline: pipeline_pb2.PipelineDescription,
                     dataset_filename: str,
                     static_resource_path: Optional[str] = None) -> Any:
    """
        Executes a binrary protobuf pipeline against a supplied d3m dataset.

    Parameters
    ----------
    pipeline: protobuf pipeline definition
    dataset_filename: path to folder containing a D3M dataset

    Returns
    -------
    The result of the pipeline execution.
    """

    _input_table.clear()
    _output_table.clear()

    # load the input dataset
    input_dataset = container.Dataset.load(dataset_filename)
    _input_table.append(input_dataset)

    steps = pipeline.steps
    for step in steps:
        # load the primitive class
        path, name = step.primitive.primitive.python_path.rsplit('.', 1)
        module = importlib.import_module(path)
        primitive_class = getattr(module, name)

        # get the static resource table, hyperparams, and instantiate the primitive
        static_resources = _get_static_resources(primitive_class, static_resource_path)
        hyperparams = _get_hyperparameters(step.primitive, primitive_class)

        primitive = None
        if static_resources:
            primitive = primitive_class(hyperparams=hyperparams, volumes=static_resources)
        else:
            primitive = primitive_class(hyperparams=hyperparams)

        # reflectively call each output method using the hyperparams
        for output in step.primitive.outputs:
            input_data = _get_input(step.primitive)
            result = getattr(primitive, output.id)(inputs=input_data)
            if type(result) is str:
                raise Exception(result)
            else:
                result = getattr(primitive, output.id)(inputs=input_data).value
                _output_table.append({output.id: result})

    # extract the final output
    output_dataref = pipeline.outputs[0].data
    return _resolve_output(output_dataref)


def execute_pipeline_file(pipeline_filename: str, dataset_filename: str, static_resource_path: str = None) -> Any:
    """
        Executes a binrary protobuf pipeline against a supplied d3m dataset.

    Parameters
    ----------
    pipeline_filename: path to binary protobuf pipeline definition
    dataset_filename: path to folder containing a D3M dataset

    Returns
    -------
    The result of the pipeline execution.
    """

    _input_table.clear()
    _output_table.clear()

    # load the protobuf pipeline def
    pipeline = _load_pipeline(pipeline_filename)

    # load the input dataset
    input_dataset = container.Dataset.load(dataset_filename)
    _input_table.append(input_dataset)

    steps = pipeline.steps
    for step in steps:
        # load the primitive class
        path, name = step.primitive.primitive.python_path.rsplit('.', 1)
        module = importlib.import_module(path)
        primitive_class = getattr(module, name)

        # get the static resource table, hyperparams, and instantiate the primitive
        static_resources = _get_static_resources(primitive_class, static_resource_path)
        hyperparams = _get_hyperparameters(step.primitive, primitive_class)

        primitive = None
        if static_resource_path:
            primitive = primitive_class(hyperparams=hyperparams, volumes=static_resources)
        else:
            primitive = primitive_class(hyperparams=hyperparams)

        # reflectively call each output method using the hyperparams
        for output in step.primitive.outputs:
            input_data = _get_input(step.primitive)
            result = getattr(primitive, output.id)(inputs=input_data).value
            _output_table.append({output.id: result})

    # extract the final output
    output_dataref = pipeline.outputs[0].data
    return _resolve_output(output_dataref)
