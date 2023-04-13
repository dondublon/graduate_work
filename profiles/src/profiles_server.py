import logging
import subprocess
from concurrent import futures
import os

import grpc
import sentry_sdk

from config import settings
from logger import logger
from grpc_files import profiles_pb2, profiles_pb2_grpc
from services_profiles.user_service import UserService


class Profiles(profiles_pb2_grpc.ProfilesServicer):
    async def Register(self, request, context):
        try:
            logger.info("!!!!!!!!!!!!!!!!!TEST")
            await UserService.register(id_=request.id, first_name=request.first_name,
                                       father_name=request.father_name, family_name=request.family_name,
                                       phone=request.phone,
                                       email=request.email)
            # noinspection PyUnresolvedReferences
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return profiles_pb2.BooleanReply(success=False)

    async def Get(self, request, context):
        user = await UserService.get_by_id(request.id)
        if user:
            reply = profiles_pb2.UserReply(**user)
            print("Got user ok")
            return reply
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User with {request.id} not found.')
            reply = profiles_pb2.UserReply()
            return reply

    async def ChangeEMail(self, request, context):
        try:
            await UserService.change_email(user_id=request.user_id, email=request.email)
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error updating user email {request.user_id}: {e}')
            return profiles_pb2.BooleanReply()


    async def UpdateProfile(self, request, context):
        try:
            await UserService.update(user_id=request.user_id, first_name=request.first_name,
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

    async def DeleteProfile(self, request, context):
        try:
            result = await UserService.delete_profile(request.id)
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error updating user {request.id}: {e}')
            return profiles_pb2.BooleanReply(success=False)

    @classmethod
    def get_avatar_path(cls, user_id, extension):
        """file extension with dot"""
        return f'{settings.avatar_path}/{user_id}{extension}'

    @classmethod
    def get_existing_avatar_path(cls, user_id):
        p = subprocess.Popen(f'ls {settings.avatar_path}/{user_id}.*', shell=True, stdout=subprocess.PIPE)
        files = [s.strip() for s in p.stdout.readlines()]
        if len(files) == 0:
            return f'{settings.avatar_path}/default.jpeg'
        elif len(files) > 1:
            logger.warn('More than one avatar for %s', user_id)
        return files[0]

    def UploadAvatar(self, request, context):
        """file extension with dot"""
        filepath = self.get_avatar_path(request.metadata.user_id, request.metadata.file_extension)
        # TODO Make only one file allowed.
        try:
            with open(filepath, 'wb') as f:
                f.write(request.chunk_data)
            return profiles_pb2.BooleanReply(success=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error uploading : {e}')
            return profiles_pb2.BooleanReply(success=False)

    def DownloadAvatar(self, request, context):
        """From request:
        id
        """
        chunk_size = 5 * 1024 * 1024

        filepath = self.get_existing_avatar_path(request.id)
        name, ext = os.path.splitext(filepath)
        logger.info(f'Current directory {os.path.abspath(".")}')
        with open(filepath, mode="rb") as f:
            logger.info(f'Retrieving the file {filepath}')
            chunk = f.read(chunk_size)
            if chunk:
                entry_response = profiles_pb2.FileResponse(chunk_data=chunk, file_extension=ext)
                return entry_response
            else:
                return


def serve():
    port = str(settings.service_port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profiles_pb2_grpc.add_ProfilesServicer_to_server(Profiles(), server)
    server.add_insecure_port('[::]:' + port)
    init_logging()
    server.start()
    logger = logging.getLogger(__name__)
    logger.info("Server started, listening on %s", port)
    logger.info("Postgres host %s, port %s, and schema: %s", settings.pg_host, settings.pg_port, settings.pg_schema)

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
