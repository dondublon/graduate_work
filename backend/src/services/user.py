"""
A service for backed that send requests to Profiles service.
"""

import grpc
from grpc import Call

from .profiles import ProfilesService
from core.config import settings, logger
import profiles_pb2
import profiles_pb2_grpc
from .service_types import RegisterAuthResult
from .auth import AuthClient


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
            # TODO Delete the record on auth.
            raise e

    @classmethod
    async def register_on_profiles(cls, id_, first_name, family_name, father_name, email, phone):
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            all_attrs = {'id': id_,
                         'first_name': first_name, 'family_name': family_name, 'father_name': father_name,
                         'email': email, 'phone': phone}
            response = stub.Register(profiles_pb2.RegisterCredentials(**all_attrs))  # TODO make async

            print(f"Client received: {response.success}")
            return all_attrs

    @classmethod
    async def change_email(cls, access_token, user_id, email):
        """
        Yes, access token and user id togeher is redundant, but for the convenience.
        """
        await AuthClient.change_email(access_token, user_id, email)
        await cls._change_profiles_email(user_id, email)

    @classmethod
    async def _change_profiles_email(cls, id_, email):
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            all_attrs = {'user_id': id_, 'email': email}
            response = stub.Register(profiles_pb2.ChangeEmailRequest(**all_attrs))  # TODO make async

            print(f"Client received: {response.success}")
            return all_attrs


    @classmethod
    async def update_profile(cls, user_id, first_name, family_name, father_name, phone):
        """Without email"""
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)

            request = profiles_pb2.UpdateProfileRequest(user_id=user_id,
                                                        first_name=first_name,
                                                        family_name=family_name,
                                                        father_name=father_name,
                                                        phone=phone)

            response = stub.UpdateProfile(request)  # TODO make async

            print(f"Client received: {response.success}")


    @classmethod
    async def get_profile(cls, user_id):
        """Without email
        """
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)

            request = profiles_pb2.GettingRequest(id=user_id)

            response = stub.Get(request)  # TODO make async
            print(f"Client received: {response}")
            if isinstance(response, profiles_pb2.UserReply):
                return response
            elif isinstance(response, profiles_pb2.ErrorReply):  # Doesn works yet
                return None


