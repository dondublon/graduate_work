from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class BooleanReply(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ChangeEmailRequest(_message.Message):
    __slots__ = ["email", "user_id"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class ErrorReply(_message.Message):
    __slots__ = ["details", "status"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    details: str
    status: int
    def __init__(self, details: _Optional[str] = ..., status: _Optional[int] = ...) -> None: ...

class FileMetadata(_message.Message):
    __slots__ = ["file_extension", "user_id"]
    FILE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    file_extension: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., file_extension: _Optional[str] = ...) -> None: ...

class FileResponse(_message.Message):
    __slots__ = ["chunk_data", "file_extension"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    FILE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    file_extension: str
    def __init__(self, chunk_data: _Optional[bytes] = ..., file_extension: _Optional[str] = ...) -> None: ...

class GettingProfilesRequest(_message.Message):
    __slots__ = ["users_id"]
    USERS_ID_FIELD_NUMBER: _ClassVar[int]
    users_id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, users_id: _Optional[_Iterable[str]] = ...) -> None: ...

class GettingRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RegisterCredentials(_message.Message):
    __slots__ = ["email", "family_name", "father_name", "first_name", "id", "phone"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    FATHER_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    email: str
    family_name: str
    father_name: str
    first_name: str
    id: str
    phone: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        first_name: _Optional[str] = ...,
        family_name: _Optional[str] = ...,
        father_name: _Optional[str] = ...,
        phone: _Optional[str] = ...,
        email: _Optional[str] = ...,
    ) -> None: ...

class UpdateProfileRequest(_message.Message):
    __slots__ = ["family_name", "father_name", "first_name", "phone", "user_id"]
    FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    FATHER_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    family_name: str
    father_name: str
    first_name: str
    phone: str
    user_id: str
    def __init__(
        self,
        user_id: _Optional[str] = ...,
        first_name: _Optional[str] = ...,
        family_name: _Optional[str] = ...,
        father_name: _Optional[str] = ...,
        phone: _Optional[str] = ...,
    ) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ["chunk_data", "metadata"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    metadata: FileMetadata
    def __init__(
        self, metadata: _Optional[_Union[FileMetadata, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...
    ) -> None: ...

class UserReply(_message.Message):
    __slots__ = ["email", "family_name", "father_name", "first_name", "id", "phone"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    FATHER_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    email: str
    family_name: str
    father_name: str
    first_name: str
    id: str
    phone: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        first_name: _Optional[str] = ...,
        family_name: _Optional[str] = ...,
        father_name: _Optional[str] = ...,
        phone: _Optional[str] = ...,
        email: _Optional[str] = ...,
    ) -> None: ...
