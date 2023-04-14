import uuid
from typing import Optional

from pydantic import BaseModel, Field


class ProfilesOut(BaseModel):
    """
    Модель используется в response_model при
    пагинации метода GET "/user/profiles" (вывод информации о пользователях)
    """
    id: str
    email: str
    firstName: str
    familyName: str
    fatherName: Optional[str]
    phone: Optional[str]
