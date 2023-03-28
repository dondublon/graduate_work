import json
from typing import Iterable

import requests

from build.config import settings
from .types_ import User


def get_token(login, password):
    """Token for authorization service"""
    login_url = f"{settings.auth_protocol_host_port}{settings.auth_login_url}"
    result = requests.post(login_url,
                           data=json.dumps({"login": login, "password": password}),
                           headers={"Content-Type": "application/json"})
    return result.json().get("access_token")


class AuthHelper:
    def get_users_emails(self, users_uuids: list[str] = ["*"]) -> Iterable[User]:
        """We need email here. If users list is "all", we get each user."""
        full_url = f"{settings.auth_protocol_host_port}{settings.auth_emails_url}"
        login = settings.auth_login
        password = settings.auth_password
        a_token = get_token(login, password)
        if not a_token:
            raise PermissionError("Unauthorized for authorization service")
        if users_uuids is None:
            users_uuids = ['*']

        response = requests.get(full_url, data=json.dumps({"users_id": users_uuids}),
                                headers={'Authorization': f"Bearer {a_token}",  'Content-Type': 'application/json'})
        emails = response.json()["emails"]
        result = [User(email=email) for email in emails]
        return result


auth_helper = AuthHelper()
