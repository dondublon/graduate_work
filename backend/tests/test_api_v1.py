"""Integration tests with launched services"""
import json
import os


import requests

from common import TestBackendCommon


class UGCTest(TestBackendCommon):
    def test_add_like(self):
        result = requests.post(
            f"http://{self.host_port}/v1/likes/add",
            headers={"user_uuid": "d99cfebe-0f2c-4098-b5aa-b27229943f2b"},
            json={"movie": "391ae61e-5bce-41f8-b01a-9238c7831f21", "value": 3},
        )
        self.assertEqual(result.status_code, 200)
        obj = json.loads(result.json())
        self.assertTrue(obj["success"])

    def test_remove_like(self):
        result = requests.delete(
            f"http://{self.host_port}/v1/likes/remove",
            headers={"user_uuid": "d99cfebe-0f2c-4098-b5aa-b27229943f2b"},
            json={
                "id": "391ae61e-5bce-41f8-b01a-9238c7831f21",
            },
        )
        self.assertEqual(result.status_code, 200)
        obj = json.loads(result.json())
        self.assertTrue(obj["success"])

    def test_add_review_like(self):
        """To launch this test, manually disable aunthorisation mechahism in
        backend/src/api/v1/review_likes.py / add."""
        result = requests.post(
            f"http://{self.host_port}/v1/review_likes/add",
            headers={"user_uuid": "d99cfebe-0f2c-4098-b5aa-b27229943f2b"},
            json={
                "movie": "391ae61e-5bce-41f8-b01a-9238c7831f21",
                "value": 3,
                "review": "63ff480aa96c3ea499bc01242",
                "review_author_id": "d96f4d59-12d4-419c-967d-fd62c41cc6b0",
            },
        )
        self.assertEqual(result.status_code, 200)
        obj = json.loads(result.json())
        self.assertTrue(obj["success"])

    def test_add_bookmark(self):
        response_reg, user_obj = self._register()
        assert 200 <= response_reg.status_code < 300  # this is not a test assert
        response_reg_json = json.loads(response_reg.json())
        # region add bookmark
        url = os.environ['BACKEND_BOOKMARK_ADD']
        bm_add_url = f"{self.full_host}{url}"
        movie_id = "803c794c-ddf0-482d-b2c2-6fa92da4c5e2"
        obj = {"movie": movie_id}
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {response_reg_json["access_token"]}'}
        response_bm_add = requests.post(bm_add_url, headers=headers, json=obj)
        # second inserting. There is an unique index, only one record will be eventually:
        requests.post(bm_add_url, headers=headers, json=obj)
        # endregion
        status = response_bm_add.status_code
        status_ok = 200 <= status < 300
        self.assertTrue(status_ok)

        # region Getting
        url = os.environ['BACKEND_BOOKMARK_LIST']
        bm_list_url = f'{self.full_host}{url}'
        obj = {"id": movie_id}
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {response_reg_json["access_token"]}'}
        response_bm_add = requests.get(bm_list_url, headers=headers, json=obj)

        list_json = response_bm_add.json()
        self.assertTrue(list_json['success'])
        obj_list = list_json['objects_list']
        print("user id", response_reg_json['inserted_id'])
        self.assertEqual(len(obj_list), 1)
        self.assertEqual(obj_list[0]['user'], response_reg_json['inserted_id'])
        # endregion