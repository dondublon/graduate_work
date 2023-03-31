# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import profiles_pb2 as profiles__pb2


class ProfilesStub(object):
    """The greeting service definition.
    Sends a greeting
    rpc SayHello (HelloRequest) returns (HelloReply) {}
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Register = channel.unary_unary(
                '/profiles.Profiles/Register',
                request_serializer=profiles__pb2.RegisterCredentials.SerializeToString,
                response_deserializer=profiles__pb2.RegisterReply.FromString,
                )


class ProfilesServicer(object):
    """The greeting service definition.
    Sends a greeting
    rpc SayHello (HelloRequest) returns (HelloReply) {}
    """

    def Register(self, request, context):
        """rpc SayHelloStreamReply (HelloRequest) returns (stream HelloReply) {}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProfilesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=profiles__pb2.RegisterCredentials.FromString,
                    response_serializer=profiles__pb2.RegisterReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'profiles.Profiles', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Profiles(object):
    """The greeting service definition.
    Sends a greeting
    rpc SayHello (HelloRequest) returns (HelloReply) {}
    """

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/profiles.Profiles/Register',
            profiles__pb2.RegisterCredentials.SerializeToString,
            profiles__pb2.RegisterReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
