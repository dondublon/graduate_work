import datetime
from enum import IntEnum
import json
from typing import Iterable

from .connection import connection
from .types_ import NotificationPattern

class InvokationType(IntEnum):
    BY_EVENT = 1
    BY_TIME = 2
    MANUAL = 3


class DBHelper:
    def __init__(self, connection):
        self.connection = connection

    def choose_event_pattern(self, event_type) -> NotificationPattern:
        cur = self.connection.cursor()
        sql = f"SELECT id, pattern_file, actual_time, settings_" \
              f" FROM notification_pattern" \
              f" WHERE type_={InvokationType.BY_EVENT.value}" \
              f" AND CAST(settings_::json->'event_type' AS VARCHAR) = '\"{event_type}\"'"
        # We expect only ine result here
        cur.execute(sql)
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No event pattern for event {event_type}")
        # noinspection PyArgumentList
        return NotificationPattern(**row)


    def add_notification_event(self, message_id, pattern_id):
        cur = self.connection.cursor()
        sql = f"INSERT INTO notification_event (pattern, source, start_time)" \
              f" VALUES (%s, %s, %s)"
        data = (pattern_id, json.dumps({"message_id": message_id}), datetime.datetime.now())
        cur.execute(sql, data)
        self.connection.commit()

    def get_time_patterns(self) -> Iterable[NotificationPattern]:
        sql = f"SELECT * FROM notification_pattern WHERE type_={InvokationType.BY_TIME.value}"
        cur = self.connection.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        # noinspection PyArgumentList
        return [NotificationPattern(**item) for item in result]

    def already_was_msg_id(self, message_id) -> bool:
        sql = f"SELECT COUNT(*) FROM notification_event WHERE " \
              f"CAST(source::json->'message_id' AS VARCHAR)='\"{message_id}\"'"
        cur = self.connection.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        count = int(row["count"])
        return count > 0

db_helper = DBHelper(connection)