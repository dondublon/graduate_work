from typing import TypedDict


class User(TypedDict):
    email: str


class NotificationPattern(TypedDict):
    id: str
    pattern_file: str
    actual_time: int
    settings_: dict

