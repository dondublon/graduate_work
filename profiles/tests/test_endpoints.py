"""
Integration tests
"""
from unittest import TestCase
import uuid

import grpc
import names
# import grpc_
import profiles_pb2, profiles_pb2_grpc
#profiles_pb2 = grpc_.profiles_pb2
#profiles_pb2_grpc = grpc_.profiles_pb2_grpc
# TODO Use host from env
from .randoms import random_email, random_phone
from ..src.utils.reply import reply_to_dict  # TODO fix path

class TestEndpoints(TestCase):
    def _register(self, id_):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            name1 = names.get_first_name()
            name2 = names.get_last_name()
            name3 = names.get_first_name()
            email = random_email()
            phone = random_phone()
            all_attrs = {'id':id_,
                'first_name': name1, 'family_name':name2, 'father_name':name3,
                'email':email, 'phone':phone}
            response = stub.Register(profiles_pb2.RegisterCredentials(**all_attrs))

            print(f"Client received: {response.success}")
            return all_attrs

    def _get(self, id_):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            response = stub.Get(profiles_pb2.GettingRequest(
                id=id_))

            print(f"Client received: {response}")
            return response

    def test_register_get_delete(self):
        id_ = str(uuid.uuid4())
        inserted = self._register(id_)
        got = self._get(id_)
        got_dict = reply_to_dict(got)
        self.assertDictEqual(inserted, got_dict)

