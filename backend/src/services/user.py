"""
A service for backed that send requests to Profiles service.
"""
import grpc
from .profiles import ProfilesService
from core.config import settings
import profiles_pb2
import profiles_pb2_grpc


class UserService(ProfilesService):
    @classmethod
    async def register(cls, first_name, family_name, father_name, email, phone):
        with grpc.insecure_channel(settings.profiles_host_port) as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            all_attrs = {'first_name': first_name, 'family_name': family_name, 'father_name': father_name,
                         'email': email, 'phone': phone}  # TODO Add phone later.
            response = stub.Register(profiles_pb2.RegisterCredentials(**all_attrs))  # TODO make async

            print(f"Client received: {response.success}")
            return all_attrs