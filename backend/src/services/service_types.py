import uuid

class RegisterAuthResult(NamedTuple):
    id_: uuid.UUID | None
    access_token: str | None

