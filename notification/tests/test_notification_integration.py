"""To run in container but not tested yet."""
import json
import os
import time
from unittest import TestCase
from uuid import uuid4

import pika
import psycopg
from psycopg.rows import dict_row


class TestMain(TestCase):
    def setUp(self) -> None:
        self.connection = psycopg.connect(
            host=os.environ["NOTIFICATION_PG_HOST"],
            port=os.environ["NOTIFICATION_PG_PORT"],
            user=os.environ["NOTIFICATION_PG_USER"],
            password=os.environ["NOTIFICATION_PG_PASSWORD"],
            dbname="notification",
            row_factory=dict_row,
        )

        self.connection_auth = psycopg.connect(
            host=os.environ["PG_HOST"],
            port=os.environ["PG_PORT"],
            user=os.environ["PG_USER"],
            password=os.environ["PG_PASSWORD"],
            dbname="movies_database",
            row_factory=dict_row,
        )

    def send_to_rmq(self):
        broker_host = os.environ["BROKER_HOST"]
        queue_name = os.environ["QUEUE_NAME"]
        connection = pika.BlockingConnection(pika.ConnectionParameters(broker_host))
        channel = connection.channel()

        print("Send json-compatible string")
        channel.queue_declare(queue=queue_name, durable=True)
        user = self.get_1st_user()
        payload = {
            "event_type": "review_like",
            "author_id": str(user["id"]),  # from the file
            "review": "63ff480aa96c3ea499bc0124",
        }
        message_id = str(uuid4())
        message = json.dumps({"message_id": message_id, "payload": payload})
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message.encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
        print(f" [x] Sent '{message}'")
        connection.close()
        return message_id

    def test_main(self):
        message_id = self.send_to_rmq()
        # Wait for 3 seconds to process everything.
        time.sleep(3)
        # We take row for last 100 entries and find our:
        inserted_row = self.find_in_last_entries(100, message_id)
        self.assertIsNotNone(inserted_row)

    def find_in_last_entries(self, count, message_id):
        cur = self.connection.cursor()
        sql = (
            f"SELECT * FROM notification_event"
            f" WHERE"
            f" CAST(source::json->'message_id' AS VARCHAR) = '\"{message_id}\"'"
            f" ORDER BY start_time DESC LIMIT 100"
        )
        print(sql)
        cur.execute(sql)
        row = cur.fetchone()
        return row
    def get_1st_user(self):
        sql = "SELECT * FROM auth.users LIMIT 1"
        cur = self.connection_auth.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        return result