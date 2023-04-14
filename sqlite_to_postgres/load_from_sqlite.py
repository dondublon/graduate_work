import sqlite3

from models import (
    FilmWork,
    Person,
    Genre,
    GenreFilmWork,
    FilmWorkPerson,
)


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    def _get_data_from_table(self, table_name):
        self._cursor.execute("SELECT * FROM {table_name};".format(table_name=table_name))
        data = []
        while True:
            rows = self._cursor.fetchmany(100)
            if len(rows) > 0:
                data += rows
            else:
                return data

    def load_movies(self):
        data = self._get_data_from_table("film_work")
        data = list(FilmWork(**kwargs) for kwargs in data)
        return data

    def load_person(self):
        data = self._get_data_from_table("person")
        data = list(Person(**kwargs) for kwargs in data)
        return data

    def load_genre(self):
        data = self._get_data_from_table("genre")
        data = list(Genre(**kwargs) for kwargs in data)
        return data

    def load_genre_film_work(self):
        data = self._get_data_from_table("genre_film_work")
        data = list(GenreFilmWork(**kwargs) for kwargs in data)
        return data

    def load_person_film_work(self):
        data = self._get_data_from_table("person_film_work")
        data = list(FilmWorkPerson(**kwargs) for kwargs in data)
        return data
