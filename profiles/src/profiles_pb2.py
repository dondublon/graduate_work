# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: profiles.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eprofiles.proto\x12\x08profiles\"}\n\x13RegisterCredentials\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x13\n\x0b\x66\x61mily_name\x18\x03 \x01(\t\x12\x13\n\x0b\x66\x61ther_name\x18\x04 \x01(\t\x12\r\n\x05phone\x18\x05 \x01(\t\x12\r\n\x05\x65mail\x18\x06 \x01(\t\" \n\rRegisterReply\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x1c\n\x0eGettingRequest\x12\n\n\x02id\x18\x01 \x01(\t\"s\n\tUserReply\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x13\n\x0b\x66\x61mily_name\x18\x03 \x01(\t\x12\x13\n\x0b\x66\x61ther_name\x18\x04 \x01(\t\x12\r\n\x05phone\x18\x05 \x01(\t\x12\r\n\x05\x65mail\x18\x06 \x01(\t\"\x1d\n\nErrorReply\x12\x0f\n\x07\x64\x65tails\x18\x01 \x01(\t2\x88\x01\n\x08Profiles\x12\x44\n\x08Register\x12\x1d.profiles.RegisterCredentials\x1a\x17.profiles.RegisterReply\"\x00\x12\x36\n\x03Get\x12\x18.profiles.GettingRequest\x1a\x13.profiles.UserReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'profiles_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTERCREDENTIALS._serialized_start=28
  _REGISTERCREDENTIALS._serialized_end=153
  _REGISTERREPLY._serialized_start=155
  _REGISTERREPLY._serialized_end=187
  _GETTINGREQUEST._serialized_start=189
  _GETTINGREQUEST._serialized_end=217
  _USERREPLY._serialized_start=219
  _USERREPLY._serialized_end=334
  _ERRORREPLY._serialized_start=336
  _ERRORREPLY._serialized_end=365
  _PROFILES._serialized_start=368
  _PROFILES._serialized_end=504
# @@protoc_insertion_point(module_scope)