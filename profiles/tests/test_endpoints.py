"""
Integration tests
"""
from unittest import TestCase
import uuid

import grpc
# import grpc_
from grpc_ import profiles_pb2, profiles_pb2_grpc
#profiles_pb2 = grpc_.profiles_pb2
#profiles_pb2_grpc = grpc_.profiles_pb2_grpc
# TODO Use host from env


class TestEndpoints(TestCase):
    def test_register(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            response = stub.Register(profiles_pb2.RegisterCredentials(
                id='beab23a8-08fa-4981-8f81-4e9c92969b40',
                first_name='Иван', family_name='Иванов', father_name='Иванович',
                email='yandex@forever.ru', phone='+79173712345'))

            print(f"Client received: {response.success}")

    def test_get(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = profiles_pb2_grpc.ProfilesStub(channel)
            response = stub.Get(profiles_pb2.GettingRequest(
                id='ec4ce37b-8c60-4f7a-8209-2cff3d8452c0'))

            print(f"Client received: {response}")