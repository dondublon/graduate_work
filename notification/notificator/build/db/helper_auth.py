import json
from typing import TypedDict, Iterable

import aiohttp
import requests

from build.config import settings


class User(TypedDict):
    email: str


async def get_token():
    """Token for authorization service"""
    login = settings.auth_login
    password = settings.auth_password
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_login_url}"
    async with aiohttp.ClientSession() as session:
        async with session.post(login_url,
                        data=json.dumps({"login": login, "password": password}),
                        headers={"Content-Type": "application/json"}) as resp:
            json_obj = await resp.json()
        a_token = json_obj.get("access_token")
        return a_token
    # result = requests.post(login_url,
    #                      data=json.dumps({"login": login, "password": password}),
    #                     headers={"Content-Type": "application/json"})
    # return result.json().get("access_token")


class AuthHelper:
    async def get_users_emails(self, users_uuids: list[str]=None) -> Iterable[User]:
        """We need email here. If users list is "all", we get each user."""
        full_url = f"{settings.auth_protocol_host_port}{settings.auth_emails_url}"
        a_token = await get_token()
        if not a_token:
            raise PermissionError("Unauthorized for authorization service")
        if users_uuids is None:
            users_uuids = ['*']
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, data=json.dumps({"users_id": users_uuids}),
                                   headers={'Authorization': f"Bearer {a_token}",  'Content-Type': 'application/json'}) as resp:
                response_json = await resp.json()
        # response = requests.get(full_url, data=json.dumps({"users_id": users_uuids}),
        #                             headers={'Authorization': f"Bearer {a_token}",  'Content-Type': 'application/json'})
        emails = response_json["emails"]
        result = [{"email": email} for email in emails]
        return result


auth_helper = AuthHelper()
