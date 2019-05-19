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
from typing import List, Dict, Set, Any, Optional, Tuple
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
from d3m.metadata import pipeline as metadata_pipeline, pipeline_run
from ta3ta2_api import utils

import frozendict

_logger = logging.getLogger(__name__)


def _load_pipeline(filename: str) -> pipeline_pb2.PipelineDescription:
    f = open(filename, "rb")
    pipeline = pipeline_pb2.PipelineDescription()
    pipeline.ParseFromString(f.read())
    f.close()
    return pipeline


def _load_inputs(dataset_filenames: List[str]) -> List[container.Dataset]:
    input_datasets = []
    for dataset_filename in dataset_filenames:
        input_dataset = container.Dataset.load(dataset_filename)
        input_datasets.append(input_dataset)
    return input_datasets


def _fit(pipeline: metadata_pipeline.Pipeline, input_dataset: List[container.Dataset], volumes_dir: Optional[str] = None) -> Tuple[Optional[runtime.Runtime], Optional[runtime.Result]]:
    hyperparams = None
    random_seed = 0

    fitted_runtime, _, result = runtime.fit(
        pipeline, None, input_dataset, hyperparams=hyperparams, random_seed=random_seed,
        volumes_dir=volumes_dir, context=metadata_base.Context.TESTING, runtime_environment=pipeline_run.RuntimeEnvironment()
    )

    if result.has_error():
        raise result.error

    return fitted_runtime, result


def _produce(fitted_pipeline: runtime.Runtime, input_dataset: List[container.Dataset]) -> container.DataFrame:
    predictions, result = runtime.produce(fitted_pipeline, input_dataset)
    if result.has_error():
        raise result.error
    return predictions


def execute_pipeline(pipeline: pipeline_pb2.PipelineDescription,
                     dataset_filenames: List[str],
                     static_resource_path: Optional[str] = None) -> Any:
    """
        Executes a binary protobuf pipeline against a supplied d3m dataset using the d3m common runtime.

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

    # load the data
    inputs = _load_inputs(dataset_filenames)

    # fit and produce
    fitted_pipeline, _ = _fit(pipeline_d3m, inputs, volumes_dir=static_resource_path)
    result = _produce(fitted_pipeline, inputs)

    return result


def execute_pipeline_file(pipeline_filename: str,
                          dataset_filenames: List[str],
                          static_resource_path: str = None) -> Any:
    """
        Executes a binary protobuf pipeline against a supplied d3m dataset using the d3m common runtime.

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
