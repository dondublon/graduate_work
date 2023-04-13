import logging
from logging import getLogger

from flask import current_app

from build.common_send import send_all
from build.db.helper import db_helper
from build.db.helper_auth import auth_helper

logger = getLogger()
logging.basicConfig(level=logging.INFO)


def on_time():
    # if SomeCheck():
        # Place check here, is we really need to send something
        # We need to scan notification_patterns, read condition there
        # then scan our UGC database and check for condition is True.
        current_app.logger.info("Invoked on time")
        users = auth_helper.get_users_emails(['*'])
        patterns = db_helper.get_time_patterns()
        send_all(users, patterns)
