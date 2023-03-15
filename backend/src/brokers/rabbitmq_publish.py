import json
import logging

import pika

from brokers.rabbitmq import RabbitmqConnection
from helpers.uuid_generate import generate_uuid

logger = logging.getLogger(__name__)


def rabbitmq_publish(rabbitmq_host: str, queue: str, payload: dict):
    rabbitmq = RabbitmqConnection(rabbitmq_host)
    rabbitmq_conn = rabbitmq.init_rabbitmq_connection()
    rabbitmq_channel = rabbitmq_conn.channel()

    rabbitmq_channel.queue_declare(queue=queue, durable=True)

    body = {
        "message_id": generate_uuid(),
        "payload": payload
    }

    logger.info(f"RABBITMQ body: {body}")
    rabbitmq_channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(body).encode(),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )
    rabbitmq_conn.close()

    logger.info(f"{body.get('message_id')} successfully publish to {rabbitmq_host}")
    return

