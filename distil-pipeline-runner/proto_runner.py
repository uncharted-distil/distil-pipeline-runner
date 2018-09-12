#!/bin/bash

import time
import os
import sys
from typing import List, Dict, Any
from concurrent import futures

import importlib
import pipeline_pb2
import pipeline_pb2_grpc
import value_pb2
import value_pb2_grpc

from d3m import container
from d3m.metadata import base as metadata_base

import frozendict


input_table: List[container.Dataset] = []
output_table: List[Dict[str, Any]] = []

def resolve_output(dataref: str) -> List[Dict[str, Any]]:
    # on inputs use the input dataset, on subsequent
    dataref_parts = dataref.split(".")
    if dataref_parts[0] == 'inputs':
        return input_table[int(dataref_parts[1])]
    if dataref_parts[0] == 'steps':
        return output_table[int(dataref_parts[1])][dataref_parts[2]]
    return []

def get_input(primitive_step: pipeline_pb2.PrimitivePipelineDescriptionStep) -> List[Dict[str, Any]]:
    # get the input data reference
    inputs = primitive_step.arguments['inputs']
    dataref = inputs.container.data
    return resolve_output(dataref)

def get_hyperparameters(primitive_step: pipeline_pb2.PrimitivePipelineDescriptionStep, primitive_class: frozendict.FrozenOrderedDict) -> Any:
    # parse out hyperparameter structures and initialize with defaults
    primitive_hyperparams_class = primitive_class.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
    hyperparams = primitive_hyperparams_class.defaults()
    new_hyperparams = dict(hyperparams)

    # iterate over entries and add values to hyperparameter struct
    for hyperparam_key, hyperparam_value in primitive_step.hyperparams.items():
        if hyperparam_value.WhichOneof('argument') == 'value':
            parsed_param = get_raw_hyperparameter(hyperparam_value.value.data.raw)
            new_hyperparams[hyperparam_key] = parsed_param

    return new_hyperparams

def get_list_hyperparameter(list: value_pb2.ValueList) -> Any:
    result_list = []
    for value in list.items:
        which_value = value.WhichOneof('raw')
        if which_value == 'list':
            result_list.append(get_list_hyperparameter(value.list))
        elif which_value == 'dict':
            result_list.append(get_dict_hyperparameter(value.dict))
        else:
            result_list.append(get_raw_hyperparameter(value))

    return result_list

def get_dict_hyperparameter(dict: value_pb2.ValueDict) -> Any:
    result_dict: Dict[str, Any] = {}
    for key, value in dict.items.items():
        which_value = value.WhichOneof('raw')
        if which_value == 'list':
            result_dict[key] = get_list_hyperparameter(value.list)
        elif which_value == 'dict':
            result_dict[key] = get_dict_hyperparameter(value.dict)
        else:
            result_dict[key] = get_raw_hyperparameter(value)

    return result_dict

def get_raw_hyperparameter(value: value_pb2.ValueRaw) -> Any:
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
        return get_list_hyperparameter(value.list)
    if which_value == 'dict':
        return get_dict_hyperparameter(value.dict)

    return None

def get_static_resources(primitive_class: frozendict.FrozenOrderedDict, static_res_path: str) -> Dict[str, str]:
    # create a table of static resource paths for this primitive if specified
    volumes = {}
    for installation in primitive_class.metadata.query()['installation']:
        if installation['type'] is 'TGZ':
            volumes[installation['key']] = os.path.join(static_res_path, installation['key'])
    return volumes

def execute_pipeline(pipeline: pipeline_pb2.PipelineDescription, static_res_path: str) -> Any:
    steps = pipeline.steps
    for step in steps:
        # load the primitive class
        path, name = step.primitive.primitive.python_path.rsplit('.', 1)
        module = importlib.import_module(path)
        primitive_class = getattr(module, name)

        # get the static resource table, hyperparams, and instantiate the primitive
        static_resources = get_static_resources(primitive_class, static_res_path)
        hyperparams = get_hyperparameters(step.primitive, primitive_class)

        primitive = None
        if static_res_path:
            primitive = primitive_class(hyperparams=hyperparams, volumes=static_resources)
        else:
            primitive = primitive_class(hyperparams=hyperparams)

        # reflectively call each output method using the hyperparams
        for output in step.primitive.outputs:
            input_data = get_input(step.primitive)

            result = getattr(primitive, output.id)(inputs=input_data).value

            output_table.append({output.id: result})

    # extract the final output
    output_dataref = pipeline.outputs[0].data
    return resolve_output(output_dataref)

def load_pipeline(filename: str) -> pipeline_pb2.PipelineDescription:
    f = open(filename, "rb")
    pipeline = pipeline_pb2.PipelineDescription()
    pipeline.ParseFromString(f.read())
    f.close()
    return pipeline

def main():
    # path to pipeline file
    pipeline_filename = sys.argv[1]

    # path to dataset
    dataset_filename = sys.argv[2]

    # optional resource path
    static_resource_path = None
    if len(sys.argv) >= 4:
        static_resource_path = sys.argv[3]

    # load the protobuf pipeline def
    pipeline = load_pipeline(pipeline_filename)

    # load the input dataset
    input_dataset = container.Dataset.load(dataset_filename)
    input_table.append(input_dataset)

    # execute the pipeline
    output = execute_pipeline(pipeline, static_resource_path)

    print(output)

if __name__ == "__main__":
    main()