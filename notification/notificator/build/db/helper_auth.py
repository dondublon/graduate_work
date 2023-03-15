from typing import Iterable

import psycopg
from psycopg.rows import dict_row

from build.config import settings


class AuthHelper:
    def __init__(self, connection):
        self.connection = connection

    # TODO Make async?
    def get_all_users(self) -> Iterable[dict]:
        sql = "SELECT * FROM auth.users"
        cur = self.connection.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        for item in result:
            yield item

    # TODO Make async?
    def get_user(self, user_uuid) -> dict:
        sql = f"SELECT * FROM auth.users WHERE id='{user_uuid}'"
        cur = self.connection.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        return result


connection_auth = psycopg.connect(
    host=settings.pg_host,
    port=settings.pg_port,
    user=settings.pg_user,
    password=settings.pg_password,
    dbname=settings.pg_db_name,
    row_factory=dict_row
)


auth_helper = AuthHelper(connection_auth)
