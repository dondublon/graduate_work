import json
import os
from unittest import TestCase

import requests
import names
from randoms import random_string, random_email, random_phone
from string import ascii_letters


class TestBackend(TestCase):
    def setUp(self):
        backend_host = os.environ['BACKEND_HOST']
        backend_port = os.environ['BACKEND_PORT']
        self.full_host = f'http://{backend_host}:{backend_port}'

    def test_registration(self):
        response, obj = self._register()
        self.assertTrue(200 <= response.status_code < 300)
        print(response)

    def _register(self):
        url = os.environ['BACKEND_REGISTER_URL']
        full_url = f'{self.full_host}{url}'

        headers = {'Content-Type': 'application/json'}
        password = random_string(6, 8, ascii_letters)
        obj = {"password": password, "password_confirmation": password,
            "first_name": names.get_first_name(), "last_name": names.get_last_name(), "father_name": None,
                "email": random_email(), "phone": None}
        response = requests.post(full_url, headers=headers, json=obj)
        return response, obj

    def test_change_email(self):
        response_reg, user_obj = self._register()
        assert 200 <= response_reg.status_code < 300  # this is not a test assert
        url = os.environ['BACKEND_CHANGE_EMAIL_URL']
        full_url = f'{self.full_host}{url}'

        response_reg_json = json.loads(response_reg.json())
        new_email = random_email()
        obj = {"id": response_reg_json["inserted_id"], "email": new_email}
        headers = {'Content-Type': 'application/json', "Authorization": f'Bearer {response_reg_json["access_token"]}'}
        response = requests.post(full_url, headers=headers, json=obj)
        status = response.status_code
        self.assertTrue(200 <= status < 300)
        response_change_json = json.loads(response.json())
        self.assertTrue(response_change_json["success"])

    def test_profile_update(self):
        response_reg, user_obj = self._register()
        assert 200 <= response_reg.status_code < 300  # this is not a test assert
        url = os.environ['BACKEND_UPDATE_PROFILE_URL']
        full_url = f'{self.full_host}{url}'

        new_first_name = names.get_first_name()
        new_family_name = names.get_last_name()
        new_phone = random_phone()

        response_reg_json = json.loads(response_reg.json())
        obj = {"id": response_reg_json["inserted_id"], "first_name": new_first_name,
               "family_name": new_family_name, 'father_name':names.get_first_name(),
               "phone": new_phone}
        headers = {'Content-Type': 'application/json', "Authorization": f'Bearer {response_reg_json["access_token"]}'}
        response = requests.post(full_url, headers=headers, json=obj)
        status = response.status_code
        self.assertTrue(200 <= status < 300)
        response_change_json = json.loads(response.json())
        self.assertTrue(response_change_json["success"])
        # TODO CHeck that we got, by id.