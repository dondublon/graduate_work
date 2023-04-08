"""
Client requests to  the Auth service
"""
import json
import requests

import jwt

from core.config import settings
from .service_types import RegisterAuthResult


class AuthClient:
    @classmethod
    async def register_on_auth(cls, password, password_confirmation, email) -> RegisterAuthResult:
        # TODO Make async
        obj = {"password": password,
               "password_confirmation": password_confirmation,
               "email": email}
        full_url = f'{settings.auth_protocol_host_port}{settings.auth_register_url}'
        response = requests.post(full_url, headers={"Content-Type": "application/json"},
                                 data=json.dumps(obj))

        json_obj = response.json()
        if 200 <= response.status_code < 300:
            decoded_at = jwt.decode(json_obj["access_token"], settings.auth_secret_key, algorithms=["HS256"])
            return RegisterAuthResult(id_=decoded_at["sub"], access_token=json_obj["access_token"] )
        else:
            raise Exception(response.text)

    @classmethod
    async def change_email(cls, id_, email):
        obj = {"email": email}
        full_url = f'{settings.auth_protocol_host_port}{settings.auth_change_email}'
        response = requests.post(full_url, headers={"Content-Type": "application/json"},
                                 json=obj)
        json_obj = response.json()
        if 200 <= response.status_code < 300:
            decoded_at = jwt.decode(json_obj["access_token"], settings.auth_secret_key, algorithms=["HS256"])
        else:
            raise Exception(response.text)


