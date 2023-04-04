from concurrent import futures
import logging

import grpc

import profiles_pb2
import profiles_pb2_grpc

from config import settings
from services.user_service import UserService


class Profiles(profiles_pb2_grpc.ProfilesServicer):
    def Register(self, request, context):
        try:
            UserService.register(id_=request.id, first_name=request.first_name,
                                 father_name=request.father_name, family_name=request.family_name,
                                 phone=request.phone,
                                 email=request.email)
            return profiles_pb2.RegisterReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return profiles_pb2.ErrorReply(details=str(e))

    def Get(self, request, context):
        # noinspection PyTypeChecker

        user = UserService.get_by_id(request.id)
        if user:
            reply = profiles_pb2.UserReply(**user)
            print("Got user ok")
            return reply
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User with {request.id} not found.')
            return profiles_pb2.ErrorReply(details=f'User with {request.id} not found.')


def serve():
    port = str(settings.service_port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profiles_pb2_grpc.add_ProfilesServicer_to_server(Profiles(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    print("Postgres host and schema: ", settings.pg_host, settings.pg_port, settings.pg_schema)
    print("Postgres dsn: ", settings.profiles_pg_dsn)  # Insecure

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
