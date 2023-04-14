import json
import logging

import pika

from brokers.rabbitmq import RabbitmqConnection
from helpers.uuid_generate import generate_uuid

logger = logging.getLogger(__name__)


def rabbitmq_publish(rabbitmq_host: str, queue: str, payload: dict):
    rabbitmq = RabbitmqConnection(rabbitmq_host)
    rabbitmq_conn = rabbitmq.init_rabbitmq_connection()

    body = {
        "message_id": generate_uuid(),
        "payload": payload
    }
    try:
        rabbitmq_channel = rabbitmq_conn.channel()

        rabbitmq_channel.queue_declare(queue=queue, durable=True)

        logger.info(f"RABBITMQ body: {body}")
        rabbitmq_channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(body).encode(),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        logger.info(f"{body.get('message_id')} successfully publish to {rabbitmq_host}")
    except Exception as e:
        logger.error(f"Message for Rabbit failed. Queue={queue}, message_id={body.get('message_id')}. Check error: {e}")
    finally:
        rabbitmq_conn.close()

    return

