import logging
from logging import getLogger

import psycopg
from flask import current_app
from psycopg.rows import dict_row

from build.config import settings
from build.common_send import send_all
from build.db.helper import db_helper
from build.db.helper_auth import auth_helper

logger = getLogger()
logging.basicConfig(level=logging.INFO)


connection_notif = psycopg.connect(
    host=settings.postgres_host,
    port=settings.postgres_port,
    user=settings.postgres_user,
    password=settings.postgres_password,
    dbname=settings.postgres_db_name,
    row_factory=dict_row
)


def on_time():
    # if SomeCheck():
        # Place check here, is we really need to send something
        # We need to scan notification_patterns, read condition there
        # then scan our UGC database and check for condition is True.
        current_app.logger.info("Invoked on time")
        users = auth_helper.get_users_emails(['*'])
        patterns = db_helper.get_time_patterns()
        send_all(users, patterns)
