import uuid
from dataclasses import dataclass, field
from datetime import datetime

now = datetime.utcnow()


@dataclass(frozen=True)
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime


@dataclass(frozen=True)
class FilmWorkPerson:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime = field(default=now)
    id: uuid.UUID = field(default=uuid.uuid4())
