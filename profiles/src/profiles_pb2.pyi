from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

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
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

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
    def __init__(self, id: _Optional[str] = ..., first_name: _Optional[str] = ..., family_name: _Optional[str] = ..., father_name: _Optional[str] = ..., phone: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

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
    def __init__(self, id: _Optional[str] = ..., first_name: _Optional[str] = ..., family_name: _Optional[str] = ..., father_name: _Optional[str] = ..., phone: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...
