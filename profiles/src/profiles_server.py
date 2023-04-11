from concurrent import futures
import os

import grpc
import sentry_sdk
from fastapi import FastAPI

from config import settings
from logger import logger
from grpc_files import profiles_pb2, profiles_pb2_grpc
from services_profiles.user_service import UserService

app = FastAPI()


class Profiles(profiles_pb2_grpc.ProfilesServicer):
    def Register(self, request, context):
        try:
            UserService.register(id_=request.id, first_name=request.first_name,
                                 father_name=request.father_name, family_name=request.family_name,
                                 phone=request.phone,
                                 email=request.email)
            # noinspection PyUnresolvedReferences
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return profiles_pb2.BooleanReply(success=False)

    def Get(self, request, context):
        user = UserService.get_by_id(request.id)
        if user:
            reply = profiles_pb2.UserReply(**user)
            print("Got user ok")
            return reply
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User with {request.id} not found.')
            reply = profiles_pb2.UserReply()
            return reply

    def ChangeEMail(self, request, context):
        try:
            logger.info("Before profile update")
            UserService.change_email(user_id=request.user_id, email=request.email)
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error updating user email {request.user_id}: {e}')
            return profiles_pb2.BooleanReply()


    def UpdateProfile(self, request, context):
        try:
            logger.info("Before profile update")
            UserService.update(user_id=request.user_id, first_name=request.first_name,
                               family_name=request.family_name, father_name=request.father_name,
                               phone=request.phone)
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error updating user {request.id}: {e}')
            return profiles_pb2.BooleanReply(success=False)

    def GetProfiles(self, request, context):
        profiles = UserService.get_users_profiles(request.users_id)
        if profiles:
            for profile in profiles:
                yield profiles_pb2.UserReply(**profile)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Users with {request.users_id} not found.')
            return profiles_pb2.UserReply()

    def DeleteProfile(self, request, context):
        try:
            result = UserService.delete_profile(request.id)
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error updating user {request.id}: {e}')
            return profiles_pb2.BooleanReply(success=False)

    @classmethod
    def get_avatar_path(cls, user_id, extension):
        return f'{settings.avatar_path}/{user_id}.{extension}'

    def UploadFile(self, request, context):
        filepath = self.get_filepath(request.metadata.user_id, request.metadata.file_extension)
        # TODO Make only one file allowed.
        try:
            with open(filepath, 'wb') as f:
                f.write(request.chunk_data)
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error uploading : {e}')
            return profiles_pb2.BooleanReply(success=True)

    def DownloadAvatar(self, request, context):
        chunk_size = 5 * 1024 * 1024

        filepath = self.get_avatar_path(request.id, 'jpeg')
        if not os.path.exists(filepath):
            filepath = self.get_avatar_path('default', 'jpeg')
        logger.info(f'Current directory {os.path.abspath(".")}')
        with open(filepath, mode="rb") as f:
            logger.info(f'Retrieving the file {filepath}')
            chunk = f.read(chunk_size)
            if chunk:
                entry_response = profiles_pb2.FileResponse(chunk_data=chunk)
                return entry_response
            else:
                return


def serve():
    port = str(settings.service_port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profiles_pb2_grpc.add_ProfilesServicer_to_server(Profiles(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    logger.info("Server started, listening on %s", port)
    logger.info("Postgres host %s, port %s, and schema: %s", settings.pg_host, settings.pg_port, settings.pg_schema)
    logger.info("Postgres dsn: %s", settings.profiles_pg_dsn)  # Insecure

    server.wait_for_termination()


def init_logging():
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=settings.logstash_traces_sample_rate,
    )


if __name__ == '__main__':
    serve()
