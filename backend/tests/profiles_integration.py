import os
from unittest import TestCase

import requests
import names
from .randoms import random_string, random_email
from string import ascii_letters


class TestBackend(TestCase):
    def setUp(self):
        self.backend_host = os.environ['BACKEND_HOST']

    def test_registration(self):
        url = os.environ['AUTH_REGISTER_URL']
        full_url = f'http://{self.backend_host}{url}'


        headers = {'Content-Type': 'application/json'}
        password = random_string(6, 8, ascii_letters)
        obj = {"password": password, "password_confirmation": password,
            "first_name": names.get_first_name(), "last_name": names.get_last_name(), "father_name": None,
                "email": random_email(), "phone": None}
        response = requests.post(full_url, headers=headers, json=obj)
        print(response)