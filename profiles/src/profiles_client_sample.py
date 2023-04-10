import logging

import grpc

from grpc_files import profiles_pb2, profiles_pb2_grpc


def run_register():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to register a user ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = profiles_pb2_grpc.ProfilesStub(channel)
        response = stub.Register(profiles_pb2.RegisterCredentials(
            id='beab23a8-08fa-4981-8f81-4e9c92969b40',
            first_name='Иван', family_name='Иванов', father_name='Иванович',
            email='yandex@forever.ru', phone='+79173712345'))

        print(f"Client received: {response.success}")


if __name__ == '__main__':
    logging.basicConfig()
    run_register()
