from typing import List

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

from models import Person, FilmWork, Genre, GenreFilmWork, FilmWorkPerson


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self._connection = pg_conn

    def _save_data(self, query: str, data: List):
        with self._connection.cursor() as cursor:
            execute_batch(cursor, query, data, len(data))
            self._connection.commit()

    def save_film_work(self, data: List[FilmWork]):
        query = 'INSERT INTO content.film_work (' \
                'id, title, description, creation_date, file_path,' \
                'rating, type, created, modified' \
                ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)' \
                'ON CONFLICT (id) DO NOTHING;'
        data = [
            (
                i.id, i.title, i.description,
                i.creation_date, i.file_path,
                i.rating, i.type, i.created_at,
                i.updated_at
            ) for i in data
        ]
        self._save_data(query, data)

    def save_person(self, data: List[Person]):
        query = 'INSERT INTO content.person (' \
                'id, full_name, created, modified' \
                ') VALUES (%s, %s, %s, %s)' \
                'ON CONFLICT (id) DO NOTHING;'
        data = [
            (i.id, i.full_name, i.created_at, i.updated_at)
            for i in data
        ]
        self._save_data(query, data)

    def save_genre(self, data: List[Genre]):
        query = 'INSERT INTO content.genre (' \
                'id, name, description,' \
                'created, modified' \
                ') VALUES (%s, %s, %s, %s, %s)' \
                'ON CONFLICT (id) DO NOTHING;'
        data = [
            (i.id, i.name, i.description, i.created_at, i.updated_at)
            for i in data
        ]
        self._save_data(query, data)

    def save_genre_film_work(self, data: List[GenreFilmWork]):
        query = 'INSERT INTO content.genre_film_work (' \
                'id, film_work_id, genre_id,' \
                'created' \
                ') VALUES (%s, %s, %s, %s)' \
                'ON CONFLICT (film_work_id, genre_id) ' \
                'DO NOTHING;'
        data = [
            (i.id, i.film_work_id, i.genre_id, i.created_at)
            for i in data
        ]
        self._save_data(query, data)

    def save_film_work_person(self, data: List[FilmWorkPerson]):
        query = 'INSERT INTO content.person_film_work (' \
                'id, film_work_id, person_id, role, ' \
                'created' \
                ') VALUES (%s, %s, %s, %s, %s)' \
                'ON CONFLICT (id) ' \
                'DO NOTHING;'
        data = [
            (i.id, i.film_work_id, i.person_id, i.role, i.created_at)
            for i in data
        ]
        self._save_data(query, data)
