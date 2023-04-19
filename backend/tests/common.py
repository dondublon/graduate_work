import os
from unittest import TestCase
from string import ascii_letters

import names
import requests

from randoms import random_string, random_email


class TestBackendCommon(TestCase):
    def setUp(self):
        backend_host = os.environ["BACKEND_HOST"]
        backend_port = os.environ["BACKEND_PORT"]
        self.full_host = f"http://{backend_host}:{backend_port}"

    def _register(self):
        url = os.environ["BACKEND_REGISTER_URL"]
        full_url = f"{self.full_host}{url}"

        headers = {"Content-Type": "application/json"}
        password = random_string(6, 8, ascii_letters)
        obj = {
            "password": password,
            "password_confirmation": password,
            "first_name": names.get_first_name(),
            "family_name": names.get_last_name(),
            "father_name": None,
            "email": random_email(),
            "phone": None,
        }
        response = requests.post(full_url, headers=headers, json=obj)
        return response, obj
