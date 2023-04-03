from concurrent import futures
import logging

from sqlalchemy import select

import grpc
import profiles_pb2
import profiles_pb2_grpc
from db import get_session
from models.user import User
from config import settings



class Profiles(profiles_pb2_grpc.ProfilesServicer):

    def Register(self, request, context):
        with get_session() as session:
            new_user = User(id=request.id, first_name=request.first_name, family_name=request.family_name,
                            father_name=request.father_name,
                            # phone=request.phone,  # TODO Add later.
                            email=request.email)
            session.add(new_user)
            session.commit()

        return profiles_pb2.RegisterReply(success=True)

    def Get(self, request, context):
        # noinspection PyTypeChecker
        user_q = select(User).where(User.id == request.id)
        with get_session() as session:
            user = session.scalar(user_q)
            if user:
                as_dict = user.as_dict(to_str=True)
                reply = profiles_pb2.UserReply(**as_dict)
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
