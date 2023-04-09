import uuid
from typing import NamedTuple


class RegisterAuthResult(NamedTuple):
    id_: uuid.UUID | None
    access_token: str | None
    refresh_token: str | None
