import json
from functools import wraps
from http import HTTPStatus

import jwt
import requests
from fastapi_jwt_auth import AuthJWT

from core.config import settings
from fastapi import HTTPException, Depends
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


async def check_auth(request: Request, authorize: AuthJWT):
    data_obj = await request.json()
    current_user_in_token = authorize.get_jwt_subject()
    if current_user_in_token:
        authorize.jwt_required()
        return current_user_in_token
    email = data_obj.get("email")
    password = data_obj.get("password")
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_login_url}"
    auth_response = requests.post(
        login_url,
        data=json.dumps({"email": email, "password": password}),
        headers={"Content-Type": "application/json"},  # "Authorization": authorization,
    )
    json_obj = auth_response.json()
    a_token = json_obj.get("access_token")
    if not a_token:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)
    decoded = jwt.decode(a_token, settings.auth_secret_key, algorithms=["HS256"])
    user_uuid = decoded.get("sub")
    if not user_uuid:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)
    return user_uuid
