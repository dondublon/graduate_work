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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0eprofiles.proto\x12\x08profiles"}\n\x13RegisterCredentials\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x13\n\x0b\x66\x61mily_name\x18\x03 \x01(\t\x12\x13\n\x0b\x66\x61ther_name\x18\x04 \x01(\t\x12\r\n\x05phone\x18\x05 \x01(\t\x12\r\n\x05\x65mail\x18\x06 \x01(\t"\x1f\n\x0c\x42ooleanReply\x12\x0f\n\x07success\x18\x01 \x01(\x08"\x1c\n\x0eGettingRequest\x12\n\n\x02id\x18\x01 \x01(\t"s\n\tUserReply\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x13\n\x0b\x66\x61mily_name\x18\x03 \x01(\t\x12\x13\n\x0b\x66\x61ther_name\x18\x04 \x01(\t\x12\r\n\x05phone\x18\x05 \x01(\t\x12\r\n\x05\x65mail\x18\x06 \x01(\t"t\n\x14UpdateProfileRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x13\n\x0b\x66\x61mily_name\x18\x03 \x01(\t\x12\x13\n\x0b\x66\x61ther_name\x18\x04 \x01(\t\x12\r\n\x05phone\x18\x05 \x01(\t"-\n\nErrorReply\x12\x0f\n\x07\x64\x65tails\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\x05"4\n\x12\x43hangeEmailRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t"*\n\x16GettingProfilesRequest\x12\x10\n\x08users_id\x18\x01 \x03(\t"7\n\x0c\x46ileMetadata\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x16\n\x0e\x66ile_extension\x18\x02 \x01(\t"Q\n\x11UploadFileRequest\x12(\n\x08metadata\x18\x01 \x01(\x0b\x32\x16.profiles.FileMetadata\x12\x12\n\nchunk_data\x18\x02 \x01(\x0c":\n\x0c\x46ileResponse\x12\x12\n\nchunk_data\x18\x01 \x01(\x0c\x12\x16\n\x0e\x66ile_extension\x18\x02 \x01(\t2\xb5\x04\n\x08Profiles\x12\x43\n\x08Register\x12\x1d.profiles.RegisterCredentials\x1a\x16.profiles.BooleanReply"\x00\x12\x36\n\x03Get\x12\x18.profiles.GettingRequest\x1a\x13.profiles.UserReply"\x00\x12\x45\n\x0b\x43hangeEMail\x12\x1c.profiles.ChangeEmailRequest\x1a\x16.profiles.BooleanReply"\x00\x12I\n\rUpdateProfile\x12\x1e.profiles.UpdateProfileRequest\x1a\x16.profiles.BooleanReply"\x00\x12H\n\x0bGetProfiles\x12 .profiles.GettingProfilesRequest\x1a\x13.profiles.UserReply"\x00\x30\x01\x12\x43\n\rDeleteProfile\x12\x18.profiles.GettingRequest\x1a\x16.profiles.BooleanReply"\x00\x12\x45\n\x0cUploadAvatar\x12\x1b.profiles.UploadFileRequest\x1a\x16.profiles.BooleanReply"\x00\x12\x44\n\x0e\x44ownloadAvatar\x12\x18.profiles.GettingRequest\x1a\x16.profiles.FileResponse"\x00\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "profiles_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REGISTERCREDENTIALS._serialized_start = 28
    _REGISTERCREDENTIALS._serialized_end = 153
    _BOOLEANREPLY._serialized_start = 155
    _BOOLEANREPLY._serialized_end = 186
    _GETTINGREQUEST._serialized_start = 188
    _GETTINGREQUEST._serialized_end = 216
    _USERREPLY._serialized_start = 218
    _USERREPLY._serialized_end = 333
    _UPDATEPROFILEREQUEST._serialized_start = 335
    _UPDATEPROFILEREQUEST._serialized_end = 451
    _ERRORREPLY._serialized_start = 453
    _ERRORREPLY._serialized_end = 498
    _CHANGEEMAILREQUEST._serialized_start = 500
    _CHANGEEMAILREQUEST._serialized_end = 552
    _GETTINGPROFILESREQUEST._serialized_start = 554
    _GETTINGPROFILESREQUEST._serialized_end = 596
    _FILEMETADATA._serialized_start = 598
    _FILEMETADATA._serialized_end = 653
    _UPLOADFILEREQUEST._serialized_start = 655
    _UPLOADFILEREQUEST._serialized_end = 736
    _FILERESPONSE._serialized_start = 738
    _FILERESPONSE._serialized_end = 796
    _PROFILES._serialized_start = 799
    _PROFILES._serialized_end = 1364
# @@protoc_insertion_point(module_scope)
