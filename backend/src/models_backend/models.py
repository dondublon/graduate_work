import uuid
from typing import Optional
from pydantic import EmailStr

from .common import BaseOrjsonModel

# No need to pass 'user' here, this is for FastApi, user uuid comes
# from the request header.


class Movie(BaseOrjsonModel):
    id: uuid.UUID

# Region request models
class Like(BaseOrjsonModel):
    movie: uuid.UUID
    value: int  # 0-10


class Review(BaseOrjsonModel):
    movie: uuid.UUID
    # user: uuid.UUID
    text: str


class ReviewId(BaseOrjsonModel):
    id: uuid.UUID


class ReviewLike(BaseOrjsonModel):
    movie: uuid.UUID
    review: str
    review_author_id: uuid.UUID
    value: int  # 0-10


class Bookmark(BaseOrjsonModel):
    movie: uuid.UUID
    # user: uuid.UUID


class UserBasic(BaseOrjsonModel):
    first_name: str
    family_name: str
    father_name: Optional[str]
    phone: Optional[str]


class UserRegisterModel(UserBasic):
    password: str
    password_confirmation: str
    email: EmailStr


class ChangeEmailModel(BaseOrjsonModel):
    id: uuid.UUID
    email: EmailStr


class UserUpdateModel(UserBasic):
    id: uuid.UUID


class UserIdModel(BaseOrjsonModel):
    id: uuid.UUID


class UserProfilesModel(BaseOrjsonModel):
    users_id: list[Optional[str]]
# endregion


# region Response models
class SuccessModel(BaseOrjsonModel):
    success: bool


class InsertedSuccessModel(SuccessModel):
    inserted_id: str  # Str - because Mongo id is not compatible with Python UUID.


class UpdatedSuccessModel(SuccessModel):
    updated_id: str


class DeletedCountSuccessModel(SuccessModel):
    deleted_count: int


class ObjectsListSuccessModel(SuccessModel):
    objects_list: list


# endregion