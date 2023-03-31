from concurrent import futures
import logging

import grpc
from grpc_ import profiles_pb2
from grpc_ import profiles_pb2_grpc


class Profiles(profiles_pb2_grpc.ProfilesServicer):

    def Register(self, request, context):
        return profiles_pb2.RegisterReply(success=True) # % request.name


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profiles_pb2_grpc.add_ProfilesServicer_to_server(Profiles(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
