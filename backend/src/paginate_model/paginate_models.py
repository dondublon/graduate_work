import uuid
from typing import Optional

from pydantic import BaseModel, Field

class ProfilesOut(BaseModel):
    id: str
    email: str
    firstName: str
    familyName: str
    fatherName: Optional[str]
    phone: Optional[str]
