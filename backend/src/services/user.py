"""
A service for backed that send requests to Profiles service.
"""
import json
import uuid
from typing import NamedTuple

import grpc
import requests

from .profiles import ProfilesService
from core.config import settings
import profiles_pb2
import profiles_pb2_grpc


class RegisterAuthResult(NamedTuple):
    id_: uuid.UUID
    access_token: str


class UserService(ProfilesService):
    @classmethod
    async def register(cls, login, password, password_confirmation, first_name, family_name, father_name, email, phone):
        # Make in simultaneously?

        # Checking for password confirmation is here:
        result = await cls.register_on_auth(login, password, password_confirmation, first_name, family_name, email)
        await cls.register_on_profiles(result.id_, first_name, family_name, father_name, email, phone)

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
    async def register_on_auth(cls, login, password, password_confirmation, first_name, last_name, email) -> RegisterAuthResult:
        # TODO Make async
        obj = {"login": login, "password": password,
               "password_confirmation": password_confirmation,
               "first_name": first_name, "last_name": last_name, "email": email}
        try:
            full_url = f'{settings.auth_protocol_host_port}{settings.auth_register_url}'
            response = requests.post(full_url, headers={"Content-Type": "application/json"},
                                     data=json.dumps(obj))

            json_obj = response.json()
            return RegisterAuthResult(id_=json_obj["id"], access_token=json_obj["access_token"] )
        except Exception as e:
            raise e
