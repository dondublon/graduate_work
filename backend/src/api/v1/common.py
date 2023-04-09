from enum import Enum
import json
from functools import wraps
from http import HTTPStatus
import time
from typing import NamedTuple

import jwt
import requests
from core.config import settings
from fastapi import HTTPException
from starlette.requests import Request


def authorize(func):
    # Не получилось сделать через декоратор, из-за того, что FastAPI нужна определённая сигнатура.
    # Можно, но сложно. Этот декоратор не используется,
    @wraps(func)
    async def inner(request: Request, **kwargs):
        data_obj = await request.json()
        login = data_obj.get("login")
        password = data_obj.get("password")
        authorization = request.headers.get("Authorization")
        login_url = f"{settings.auth_protocol_host_port}/api/v1/user/login"
        auth_response = requests.post(
            login_url,
            data=json.dumps({"login": login, "password": password}),
            headers={"Content-Type": "application/json"},  # "Authorization": authorization,
        )
        json_obj = auth_response.json()
        a_token = json_obj.get("access_token")
        decoded = jwt.decode(a_token, settings.auth_secret_key, algorithms=["HS256"])
        if "access_token" in json_obj:
            return await func(request=request, **kwargs)
        else:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

    return inner


class AuthResult(NamedTuple):
    access_token: str

    @property
    def user_uuid(self):
        decoded = jwt.decode(self.access_token, settings.auth_secret_key, algorithms=["HS256"])
        user_uuid = decoded.get("sub")
        return user_uuid


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


async def check_auth(request: Request) -> AuthResult:
    data_obj = await request.json()
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_login_url}"
    if 'authorization' in request.headers:
        bearer, token = request.headers['authorization'].split(' ')
        if bearer != 'Bearer':
            raise HTTPException(HTTPStatus.BAD_REQUEST, 'Wrong authorization format')
        check_result = check_jwt(token)
        if check_result != CheckJWTResult.VALID is None:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)
        # TODO Make refresh if needed
        result = AuthResult(token)
    else:
        login = data_obj.get("login")
        password = data_obj.get("password")

        auth_response = requests.post(
            login_url,
            data=json.dumps({"login": login, "password": password}),
            headers={"Content-Type": "application/json"},  # "Authorization": authorization,
        )
        json_obj = auth_response.json()
        a_token = json_obj.get("access_token")
        if not a_token:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)
        result = AuthResult(a_token)
        if not result.user_uuid:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)
    return result
