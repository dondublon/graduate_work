"""To run in container but not tested yet."""
import json
import os
import time
from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

#import pika
from aio_pika import connect_robust, Message, DeliveryMode
import psycopg
from psycopg.rows import dict_row


class TestMain(IsolatedAsyncioTestCase):
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

    async def init_rabbitmq_connection(self):
        """Copy-paste from backend/src/brokers/rabbitmq.py"""
        broker_host = os.environ["BROKER_HOST"]
        conn_sting = f'amqp://guest:guest@{broker_host}/'
        connection = await connect_robust(conn_sting)
        return connection

    async def send_to_rmq(self):
        queue_name = os.environ["QUEUE_NAME"]
        # connection = pika.BlockingConnection(pika.ConnectionParameters(broker_host))
        connection = await self.init_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()

            print("Send json-compatible string")
            await channel.declare_queue(name=queue_name, durable=True)
            user = self.get_1st_user()
            payload = {
                "event_type": "review_like",
                "author_id": str(user["id"]),  # from the file
                "review": "63ff480aa96c3ea499bc0124",
            }
            message_id = str(uuid4())
            message = json.dumps({"message_id": message_id, "payload": payload})
            await channel.default_exchange.publish(
                # exchange="",
                Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=queue_name,
                # properties=aio_pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
            )
            print(f" [x] Sent '{message}'")
            await connection.close()
            return message_id

    async def test_main(self):
        message_id = await self.send_to_rmq()
        # Wait for 3 seconds to process everything.
        time.sleep(3)
        # We take row for last 100 entries and find our one:
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