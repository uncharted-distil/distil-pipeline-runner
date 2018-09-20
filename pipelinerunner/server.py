import time
from concurrent import futures

import grpc
import os
import uuid

import execute_pb2
import execute_pb2_grpc
import pipeline_executor as pe

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ExecuteService(execute_pb2_grpc.ExecutorServicer):

    def ExecutePipeline(self, request, context):
        print("Executing pipeline", request)

        # execute the pipeline against the data
        output = pe.execute_pipeline(request.pipelineDescription, request.inputs[0].dataset_uri)

        # get output dir
        output_path = self.get_output_path()

        # write output
        self.write_output(output_path, output)

        # return response with output path
        return execute_pb2.PipelineExecuteResponse(resultURI=output_path)

    def write_output(self, output_path, output):

        directory = os.path.dirname(output_path)

        try:
            os.stat(directory)
        except:
            os.makedirs(directory, exist_ok=True)

        output.to_csv(output_path)

    def get_output_path(self):

        output_dir = os.environ['D3MOUTPUTDIR']
        return output_dir + "/temp/" + str(uuid.uuid4())

def serve():
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
