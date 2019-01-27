import time
from concurrent import futures
import os
from typing import List, Dict, Any, Optional

import grpc
import uuid
import pandas as pd

import execute_pb2
import execute_pb2_grpc
import pipeline_executor as pe

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ExecuteService(execute_pb2_grpc.ExecutorServicer):

    def ExecutePipeline(self,
                        request: execute_pb2.PipelineExecuteRequest,
                        context: grpc.RpcContext) -> execute_pb2.PipelineExecuteResponse:
        print("Executing pipeline", request)
        verbose_primitive_output = False if os.environ.get('VERBOSE_PRIMITIVE_OUTPUT') is None else True
        static_res_path = os.environ['STATIC_RESOURCE_PATH']

        # execute the pipeline against the data
        dataset_uris = [input.dataset_uri for input in request.inputs]
        try:
            output = pe.execute_pipeline(request.pipelineDescription,
                                        dataset_uris,
                                        static_res_path,
                                        verbose_primitive_output)

            # get output dir
            output_path = self.get_output_path()

            # write output
            self.write_output(output_path, output)

            # return response with output path
            return execute_pb2.PipelineExecuteResponse(resultURI=output_path)
        except Exception as ex:
            print(ex)
            raise ex

    def write_output(self, output_path: str, output: pd.DataFrame) -> None:
        directory = os.path.dirname(output_path)
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)
        output.to_csv(output_path)

    def get_output_path(self) -> str:
        output_dir = os.environ['D3MOUTPUTDIR']
        return output_dir + "/temp/" + str(uuid.uuid4())


def serve() -> None:

    print('home exists: ' + str(os.path.exists("/home/chris")))
    print('datamart exists: ' + str(os.path.exists("/home/chris/dev/go_workspace/src/github.com/unchartedsoftware/distil/datamart")))
    print( 'datamart contents: ' + str(os.listdir('/home/chris/dev/go_workspace/src/github.com/unchartedsoftware/distil/datamart')))    

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    execute_pb2_grpc.add_ExecutorServicer_to_server(
        ExecuteService(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting gRPC server")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
