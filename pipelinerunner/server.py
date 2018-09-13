import time
from concurrent import futures

import grpc

import execute_pb2
import execute_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ExecuteService(execute_pb2_grpc.ExecutorServicer):

    def ExecutePipeline(self, request, context):
        print("Inside my DNA")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    execute_pb2_grpc.add_ExecutorServicer_to_server(
        ExecuteService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)




if __name__ == '__main__':
    serve()


