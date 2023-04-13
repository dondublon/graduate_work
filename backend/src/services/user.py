"""
A service for backed that send requests to Profiles service.
"""
import os.path

import grpc
from google.protobuf.json_format import MessageToDict

from grpc_files import profiles_pb2_grpc, profiles_pb2
from .profiles import ProfilesService
from core.config import settings, logger

from .service_types import RegisterAuthResult
from .auth import AuthClient


class NotFoundError(Exception):
    pass


class UserService(ProfilesService):
    @classmethod
    async def register(cls, password, password_confirmation, first_name, family_name, father_name, email, phone) -> RegisterAuthResult:
        # Make in simultaneously?

        # Checking for password confirmation is here:
        result = await AuthClient.register_on_auth(password, password_confirmation, email)
        # noinspection PyUnusedLocal
        try:
            await cls.register_on_profiles(result.id_, first_name, family_name, father_name, email, phone)
            return result
        except Exception as e:
            logger.error("Error on registration %s, %s", (result.id_, first_name, family_name, father_name, email, phone), e)
            raise e

    @classmethod
    async def register_on_profiles(cls, id_, first_name, family_name, father_name, email, phone):
        async with grpc.aio.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            all_attrs = {'id': id_,
                         'first_name': first_name, 'family_name': family_name, 'father_name': father_name,
                         'email': email, 'phone': phone}
            response = await stub.Register(profiles_pb2.RegisterCredentials(**all_attrs))

            logger.info(f"Client id: {id_} received")
            return all_attrs

    @classmethod
    async def change_email(cls, access_token, user_id, email):
        """
        Yes, access token and user id togeher is redundant, but for the convenience.
        """
        await AuthClient.change_email(access_token, email)
        await cls._change_profiles_email(user_id, email)
        logger.info("Email changed to %s in both places.", email)

    @classmethod
    async def _change_profiles_email(cls, id_, email):
        async with grpc.aio.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            all_attrs = {'user_id': id_, 'email': email}
            response = await stub.ChangeEMail(profiles_pb2.ChangeEmailRequest(**all_attrs))
            logger.info(f"Email changed")
            return all_attrs


    @classmethod
    async def update_profile(cls, user_id, first_name, family_name, father_name, phone):
        """Without email"""
        async with grpc.aio.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)

            request = profiles_pb2.UpdateProfileRequest(user_id=user_id,
                                                        first_name=first_name,
                                                        family_name=family_name,
                                                        father_name=father_name,
                                                        phone=phone)

            response = await stub.UpdateProfile(request)
            return


    @classmethod
    async def get_profile(cls, user_id):
        """Without email
        """
        async with grpc.aio.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)

            request = profiles_pb2.GettingRequest(id=user_id)
            try:
                response = await stub.Get(request)
                return response
            except grpc.RpcError as e:
                # noinspection PyUnresolvedReferences
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    # noinspection PyUnresolvedReferences
                    raise NotFoundError(e.details())
                else:
                    raise e

    @classmethod
    def get_profiles(cls, users_id) -> list[dict]:
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            responses = stub.GetProfiles(profiles_pb2.GettingProfilesRequest(users_id=users_id))
            cash = [MessageToDict(response) for response in responses]
            return cash

    @classmethod
    async def delete_user(cls, access_token, user_id):
        await cls._delete_from_profiles(user_id)
        logger.info('Delete from profiles - ok')
        result = AuthClient.unregister(access_token)
        logger.info('Delete from auth - ok')
        return result

    @classmethod
    async def _delete_from_profiles(cls, user_id) -> bool:
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            try:
                stub = profiles_pb2_grpc.ProfilesStub(channel)
                response = await stub.DeleteProfile(profiles_pb2.GettingRequest(id=user_id))
                return response.success
            except grpc.RpcError as e:
                # noinspection PyUnresolvedReferences
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    # noinspection PyUnresolvedReferences
                    raise NotFoundError(e.details())
                else:
                    raise e


    @classmethod
    async def upload_avatar(cls, filename, user_id, file_data: bytearray):
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            short_filename, extension = os.path.splitext(filename)
            response = stub.UploadAvatar(profiles_pb2.UploadFileRequest(
                metadata=profiles_pb2.FileMetadata(user_id=user_id, file_extension=extension),
                chunk_data=file_data))
            logger.info('upload_avatar response %s', response)
            return response

    @classmethod
    async def get_avatar(cls, user_id) -> bytearray:
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            response = stub.DownloadAvatar(profiles_pb2.GettingRequest(id=user_id))
            logger.info('get_avatar response %s', response)
            return response