import json
import os

import requests
import names

from common import TestBackendCommon
from randoms import random_email, random_phone


class TestBackend(TestBackendCommon):
    def test_registration(self):
        response, obj = self._register()
        self.assertTrue(200 <= response.status_code < 300)
        print(response)

    def test_change_email(self):
        response_reg, user_obj = self._register()
        assert 200 <= response_reg.status_code < 300  # this is not a test assert
        response_reg_json = json.loads(response_reg.json())

        url = os.environ["BACKEND_CHANGE_EMAIL_URL"]
        change_full_url = f"{self.full_host}{url}"

        user_id = response_reg_json['inserted_id']
        new_email = random_email()
        print("User id:", user_id)
        print("old email: ", user_obj["email"])
        print("new email: ", new_email)
        obj = {"id": response_reg_json["inserted_id"], "email": new_email}
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {response_reg_json["access_token"]}'}
        response = requests.post(change_full_url, headers=headers, json=obj)
        status = response.status_code
        self.assertTrue(200 <= status < 300)
        response_change_json = json.loads(response.json())
        self.assertTrue(response_change_json["success"])

    def test_profile_update(self):
        response_reg, user_obj = self._register()
        assert 200 <= response_reg.status_code < 300  # this is not a test assert
        # Region change data
        url = os.environ["BACKEND_UPDATE_PROFILE_URL"]
        change_url = f"{self.full_host}{url}"

        new_first_name = names.get_first_name()
        new_family_name = names.get_last_name()
        new_phone = random_phone()

        response_reg_json = json.loads(response_reg.json())
        # We don't need id here because we take it from authorization token.
        obj = {
            "first_name": new_first_name,
            "family_name": new_family_name,
            "father_name": names.get_first_name(),
            "phone": new_phone,
        }
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {response_reg_json["access_token"]}'}
        response_change = requests.post(change_url, headers=headers, json=obj)
        status = response_change.status_code
        status_ok = 200 <= status < 300
        if not status_ok:
            print(response_change.text)
        self.assertTrue(status_ok)
        response_change_json = json.loads(response_change.json())
        self.assertTrue(response_change_json["success"])
        # Get and check updated user:
        url = os.environ["BACKEND_GET_PROFILE_URL"]
        get_url = f"{self.full_host}{url}"
        # No id, we take it from authorization.
        response_get = requests.get(get_url, headers=headers)
        changed_user = json.loads(response_get.json())
        status_get = response_get.status_code
        status_change_ok = 200 <= status_get < 300
        self.assertTrue(status_change_ok)
        del changed_user["id"]
        del changed_user["email"]
        self.assertDictEqual(changed_user, obj)
        # endregion

        # region deleting
        del_short_url = os.environ["BACKEND_DELETE_USER_URL"]
        del_url = f"{self.full_host}{del_short_url}"
        response_del = requests.delete(del_url, headers=headers)
        status = response_del.status_code
        status_ok = 200 <= status < 300
        if not status_ok:
            print(response_del.text)
        self.assertTrue(status_ok)
        # endregion

    def test_upload_avatar(self):
        # regionregister
        response_reg, user_obj = self._register()
        assert 200 <= response_reg.status_code < 300  # this is not a test assert
        response_reg_json = json.loads(response_reg.json())
        # endregion

        # region upload
        url = os.environ["BACKEND_UPLOAD_AVATAR"]
        upload_url = f"{self.full_host}{url}"
        headers = {"Authorization": f'Bearer {response_reg_json["access_token"]}'}

        with open("some_file.jpeg", "rb") as f:
            files = {"file": f}
            response = requests.post(upload_url, files=files, headers=headers)
        with open("some_file.jpeg", "rb") as f:
            content_to_check = f.read()
        upload_response_json = json.loads(response.json())
        user_id = upload_response_json["user_id"]
        # endregion

        # region download and check
        url = os.environ["BACKEND_GET_AVATAR"]
        download_url = f"{self.full_host}{url}/{user_id}"
        print("Avatar URL", download_url)
        response = requests.get(download_url, headers=headers)
        print(response)
        self.assertEqual(content_to_check, response.content)
        # endregion
