from http import HTTPStatus

from flask import abort
from sqlalchemy.exc import DataError

from models import User


def get_users_emails(users_id: list) -> list:
    try:
        user = User.find_emails_for_users(users_id)
    except DataError:
        abort(HTTPStatus.BAD_REQUEST, "Invalid id")
    else:
        if not user:
            abort(HTTPStatus.FORBIDDEN, "Invalid token")
        return user


class EmailService:
    @classmethod
    def get_user_roles(cls, users_id: list) -> dict:
        users = get_users_emails(users_id)
        emails = {"emails": [user.email for user in users if user.email]}
        return emails
