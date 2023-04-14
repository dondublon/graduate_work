"""
Client requests to  the Auth service
"""
import json
import requests
import aiohttp

import jwt

from core.config import settings, logger
from .service_types import RegisterAuthResult


class AuthClient:
    @classmethod
    async def register_on_auth(cls, password, password_confirmation, email) -> RegisterAuthResult:
        # TODO Make async
        obj = {"password": password,
               "password_confirmation": password_confirmation,
               "email": email}
        full_url = f'{settings.auth_protocol_host_port}{settings.auth_register_url}'
        async with aiohttp.ClientSession() as session:
            async with session.post(full_url, headers={"Content-Type": "application/json"},
                                    data=json.dumps(obj)) as response:
                json_obj = await response.json()
                if 200 <= response.status < 300:
                    decoded_at = jwt.decode(json_obj["access_token"], settings.auth_secret_key, algorithms=["HS256"])
                    return RegisterAuthResult(id_=decoded_at["sub"], access_token=json_obj["access_token"],
                                              refresh_token=json_obj["refresh_token"])
                else:
                    raise Exception(response.text)

    @classmethod
    async def change_email(cls, access_token, email):
        """Request from backend to auth. """
        obj = {"email": email}
        full_url = f'{settings.auth_protocol_host_port}{settings.auth_change_email}'
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {access_token}'}
        async with aiohttp.ClientSession() as session:
            async with session.post(full_url, headers=headers,
                                    json=obj) as response:
                json_obj = await response.json()
                if 200 <= response.status < 300:
                    logger.info(json_obj.get("message"))
                    return True
                else:
                    raise Exception(response.text)

    @classmethod
    async def unregister(cls, access_token) -> bool:
        # TODO Make async

        full_url = f'{settings.auth_protocol_host_port}{settings.auth_unregister_url}'
        async with aiohttp.ClientSession() as session:
            async with session.delete(full_url, headers={"Content-Type": "application/json",
                                                      "Authorization": f'Bearer {access_token}'}) as response:

                if 200 <= response.status < 300:
                    return True
                else:
                    raise Exception(response.text)
