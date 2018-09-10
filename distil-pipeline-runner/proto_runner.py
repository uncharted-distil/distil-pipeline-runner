#!/bin/bash

import time
from typing import List, Dict, Any
from concurrent import futures

import importlib
import pipeline_pb2
import pipeline_pb2_grpc

from d3m import container

import frozendict

import sys

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
    # parse out hyperparameter structures
    primitive_hyperparams_class = primitive_class.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
    return primitive_hyperparams_class.defaults()

def execute_pipeline(pipeline) -> Any:
    steps = pipeline.steps
    for step in steps:
        # load the primitive class
        path, name = step.primitive.primitive.python_path.rsplit('.', 1)
        module = importlib.import_module(path)
        primitive_class = getattr(module, name)

        hyperparams = get_hyperparameters(step.primitive, primitive_class)
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
    pipeline_filename = sys.argv[1]
    dataset_filename = sys.argv[2]

    pipeline = load_pipeline(pipeline_filename)
    input_dataset = container.Dataset.load(dataset_filename)

    input_table.append(input_dataset)

    output = execute_pipeline(pipeline)

    cols = input_dataset['0'].columns.values
    for feature_idx in output['features']:
        print(cols[int(feature_idx)])

if __name__ == "__main__":
    main()