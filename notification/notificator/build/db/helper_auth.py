import json
from typing import TypedDict, Iterable

import aiohttp
import requests

from build.config import settings


class User(TypedDict):
    email: str


def get_token():
    """Token for authorization service"""
    login = settings.auth_login
    password = settings.auth_password
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_login_url}"
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(login_url,
    #                     data=json.dumps({"login": login, "password": password})) as resp:
    #         json_obj = await resp.json()
    #     a_token = json_obj.get("access_token")
    #     return a_token
    result = requests.post(login_url,
                         data=json.dumps({"login": login, "password": password}),
                        headers={"Content-Type": "application/json"})
    return result.json().get("access_token")


class AuthHelper:
    def get_users_emails(self, users_uuids: list[str]=None) -> Iterable[User]:
        """We need email here. If users list is "all", we get each user."""
        full_url = f"{settings.auth_protocol_host_port}{settings.auth_emails_url}"
        a_token = get_token()
        if not a_token:
            raise PermissionError("Unauthorized for authorization service")
        if True: # users_uuids is None:
            users_uuids = ['*']
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(full_url, data=json.dumps({"users": users_uuids}),
        #                            headers=f"Bearer {a_token}") as resp:
        #         response = await resp.json()
        #         return response
        result = requests.get(full_url, data=json.dumps({"users_id": users_uuids}),
                                    headers={'Authorization': f"Bearer {a_token}",  'Content-Type': 'application/json'})
        return result.json()


auth_helper = AuthHelper()
