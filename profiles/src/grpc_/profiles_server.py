from concurrent import futures
import logging
import uuid  ## TODO temporary

from sqlalchemy import select

import grpc
from grpc_ import profiles_pb2
from grpc_ import profiles_pb2_grpc
from db import get_session
from models.user import User



class Profiles(profiles_pb2_grpc.ProfilesServicer):

    def Register(self, request, context):
        with get_session() as session:
            new_user = User(id=uuid.uuid4(), first_name="qwe", family_name="weqcfsd",
                            father_name="father name", phone="+721893101924", email="dfsd@gogo.ru")
            session.add(new_user)
            session.commit()

        return profiles_pb2.RegisterReply(success=True)

    def Get(self, request, context):
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
