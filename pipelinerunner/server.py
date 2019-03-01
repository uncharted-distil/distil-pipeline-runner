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
from concurrent import futures
import os
from typing import List, Dict, Any, Optional
import logging
import logging.config

import grpc
import uuid
import pandas as pd

import execute_pb2
import execute_pb2_grpc
import pipeline_executor as pe
import logging
import datetime

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

_logger = logging.getLogger(__name__)

class ExecuteService(execute_pb2_grpc.ExecutorServicer):

    def ExecutePipeline(self,
                        request: execute_pb2.PipelineExecuteRequest,
                        context: grpc.RpcContext) -> execute_pb2.PipelineExecuteResponse:
        static_res_path = os.environ['STATIC_RESOURCE_PATH']


        _logger.info('Received execute request: \n' + str(request))

        # execute the pipeline against the data
        dataset_uris = [input.dataset_uri for input in request.inputs]
        try:
            output = pe.execute_pipeline(request.pipelineDescription,
                                        dataset_uris,
                                        static_res_path)

            # get output dir
            output_path = self.get_output_path()

            # write output
            self.write_output(output_path, output)

            # return response with output path
            return execute_pb2.PipelineExecuteResponse(resultURI=output_path)

        except Exception as ex:
            _logger.exception(ex)
            raise ex

    def write_output(self, output_path: str, output: pd.DataFrame) -> None:
        _logger.info('serializing output to ' + output_path)
        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)
        output.to_csv(output_path)

    def get_output_path(self) -> str:
        output_dir = os.environ['D3MOUTPUTDIR']
        return output_dir + "/temp/" + str(uuid.uuid4())


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    execute_pb2_grpc.add_ExecutorServicer_to_server(
        ExecuteService(), server)
    server.add_insecure_port('[::]:50051')
    _logger.info("Starting gRPC server")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
    _logger.info("Stopping gRPC server")


if __name__ == '__main__':
    level = logging.DEBUG if 'VERBOSE_PRIMITIVE_OUTPUT' in os.environ else logging.INFO
    logging.basicConfig(level=level)

    serve()
