import logging

from http import HTTPStatus
from uuid import UUID

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from flask import abort, current_app
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.exc import DataError

from models.user import User
from models.login_history import LoginHistory

from utils.pagination import paginate
from utils.token import block_token

logger = logging.getLogger(__name__)


def get_user_or_error(user_id: UUID) -> User:
    try:
        user = User.find_by_id(user_id)
    except DataError:
        abort(HTTPStatus.BAD_REQUEST, "Invalid id")
    else:
        if not user:
            abort(HTTPStatus.FORBIDDEN, "Invalid token")
        return user


class JWTs(BaseModel):
    access_token: str
    refresh_token: str


class UserService:
    @classmethod
    def get_tokens(cls, user: User) -> JWTs:
        return JWTs(
            access_token=create_access_token(identity=user.id),
            refresh_token=create_refresh_token(identity=user.id),
        )

    @classmethod
    def register(
        cls,
        email: str,
        password: str,
        password_confirmation: str,
        *args,
        **kwargs,
    ) -> (dict, int):
        if User.find_by_email(email):
            abort(
                HTTPStatus.BAD_REQUEST,
                "User with email {} already exists".format(email),
            )

        if len(email) <= 6 or "@" not in email:
            abort(HTTPStatus.BAD_REQUEST, "Email is incorrect")

        if password != password_confirmation:
            abort(HTTPStatus.BAD_REQUEST, "Passwords do not match")

        if len(password) < 6:
            abort(
                HTTPStatus.BAD_REQUEST,
                "Password has to contains more pr equal 6 symbols",
            )

        new_user = User(email=email, password=password)
        try:
            new_user.save()
            tokens: JWTs = cls.get_tokens(new_user)
            # TODO: notification about register
            return tokens.dict(), HTTPStatus.CREATED
        except Exception as error:
            current_app.logger.error(error)
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    @classmethod
    def login(cls, email: str, password: str, user_agent: str = None, device: str = None):
        user = User.find_by_email(email)
        if not user:
            abort(
                HTTPStatus.BAD_REQUEST,
                "User with email {} does not exist".format(email),
            )

        is_correct_password = user.verify_password(password)

        if not is_correct_password:
            abort(HTTPStatus.BAD_REQUEST, "Password is incorrect")

        tokens: JWTs = cls.get_tokens(user)

        login = LoginHistory(user_id=user.id, user_agent=user_agent, device=device)
        login.save()
        # TODO: notification about authorization

        return tokens, HTTPStatus.OK

    @classmethod
    def refresh(cls, user_id: UUID, token: dict):
        user = get_user_or_error(user_id)
        tokens: JWTs = cls.get_tokens(user)
        block_token(token["jti"], token["exp"])
        return tokens, HTTPStatus.OK

    @classmethod
    def logout(cls, user_id: UUID, token: dict) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        block_token(token["jti"], token["exp"])
        return {"message": "Token successfully revoked"}, HTTPStatus.OK

    @classmethod
    def change_password(cls, user_id: UUID, password: str) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        user.set_password(password)
        return {"message": "Password was successfully changed"}, HTTPStatus.OK

    @classmethod
    def change_email(cls, user_id: UUID, login: str) -> (dict, HTTPStatus):
        user = get_user_or_error(user_id)
        user.set_email(login)
        return {"message": "Email was successfully changed"}, HTTPStatus.OK

    @classmethod
    def get_login_histories(cls, user_id: UUID, page: int = 1, page_size: int = 10) -> dict:
        query = LoginHistory.get_sessions(user_id)
        data = paginate(query, page, page_size)
        return data

    @classmethod
    def get_user_profile(cls, user_id: UUID) -> User:
        user = get_user_or_error(user_id)
        return user

    @classmethod
    def unregister(cls, user_id: UUID) -> bool:
        result = delete(User).where(User.id==user_id)
        logger.info('User %s deleted, result: %s', user_id, result)
        return bool(result)