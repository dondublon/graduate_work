import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from load_from_sqlite import SQLiteLoader
from sqlite_to_postgres.save_into_postgres import PostgresSaver


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    movies = sqlite_loader.load_movies()
    persons = sqlite_loader.load_person()
    genres = sqlite_loader.load_genre()
    genre_film_work = sqlite_loader.load_genre_film_work()
    person_film_work = sqlite_loader.load_person_film_work()

    postgres_saver.save_film_work(movies)
    postgres_saver.save_person(persons)
    postgres_saver.save_genre(genres)
    postgres_saver.save_genre_film_work(genre_film_work)
    postgres_saver.save_film_work_person(person_film_work)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    dsl = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": os.getenv("DB_PORT", 5432),
    }
    with conn_context("db.sqlite") as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
