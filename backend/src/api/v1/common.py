from enum import Enum
import json
from http import HTTPStatus
import time
from typing import NamedTuple

import aiohttp
import jwt
from fastapi_jwt_auth import AuthJWT

from core.config import settings
from fastapi import HTTPException
from starlette.requests import Request


class AuthResult(NamedTuple):
    access_token: str
    user_uuid: str


class CheckJWTResult(Enum):
    VALID = 0
    UNDECODABLE = 1
    EXPIRED = 2


def check_jwt(token: str) -> CheckJWTResult:
    try:
        decoded_token = jwt.decode(token, settings.auth_secret_key, algorithms=["HS256"])
        if decoded_token["exp"] >= time.time():
            return CheckJWTResult.VALID
        else:
            return CheckJWTResult.EXPIRED
    except:
        return CheckJWTResult.UNDECODABLE


async def check_auth(request: Request, authorize: AuthJWT = None) -> AuthResult:
    if authorize:
        current_user_in_token = authorize.get_jwt_subject()
        if current_user_in_token:
            authorize.jwt_required()
            result = AuthResult(authorize._token, current_user_in_token)  # :( private field is bad, I know
            return result
    data_obj = await request.json()
    email = data_obj.get("email")
    password = data_obj.get("password")
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_login_url}"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            login_url,
            data=json.dumps({"email": email, "password": password}),
            headers={"Content-Type": "application/json"},  # "Authorization": authorization,
        ) as auth_response:
            json_obj = await auth_response.json()
            a_token = json_obj.get("access_token")
            if not a_token:
                raise HTTPException(HTTPStatus.UNAUTHORIZED)
            decoded = jwt.decode(a_token, settings.auth_secret_key, algorithms=["HS256"])
            user_uuid = decoded.get("sub")
            if not user_uuid:
                raise HTTPException(HTTPStatus.UNAUTHORIZED)
            return AuthResult(a_token, user_uuid)


async def check_role(user_uuid: str, access_token: str) -> list:
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_role_url}?user_id={user_uuid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(login_url, headers={"Authorization": f"Bearer {access_token}"}) as response:
            result = await response.json()
            roles_list = [role.get("name").lower() for role in result]
            if settings.admin_roles.lower() not in roles_list:
                raise HTTPException(HTTPStatus.UNAUTHORIZED)
            return roles_list


async def get_email(user_uuid: str, access_token: str) -> list:
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_profile_url}?user_id={user_uuid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(login_url, headers={"Authorization": f"Bearer {access_token}"}) as response:
            email = await response.json()
            if not email.get("email"):
                raise HTTPException(HTTPStatus.NO_CONTENT)
            return email
