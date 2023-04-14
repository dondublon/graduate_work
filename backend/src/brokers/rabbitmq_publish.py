import json
import logging

from aio_pika import Message, DeliveryMode

from brokers.rabbitmq import RabbitmqConnection
from helpers.uuid_generate import generate_uuid

logger = logging.getLogger(__name__)


async def rabbitmq_publish(rabbitmq_host: str, queue: str, payload: dict) -> bool:
    rabbitmq = RabbitmqConnection(rabbitmq_host)
    rabbitmq_conn = await rabbitmq.init_rabbitmq_connection()
    async with rabbitmq_conn:
        body = {"message_id": generate_uuid(), "payload": payload}
        try:
            rabbitmq_channel = await rabbitmq_conn.channel()

            await rabbitmq_channel.declare_queue(name=queue, durable=True)

            logger.info(f"RABBITMQ body: {body}")
            await rabbitmq_channel.default_exchange.publish(
                Message(body=json.dumps(body).encode(), delivery_mode=DeliveryMode.PERSISTENT), routing_key=queue
            )

            logger.info(f"{body.get('message_id')} successfully published to {rabbitmq_host}")
            success = True
        except Exception as e:
            logger.error(
                f"Message for Rabbit failed. Queue={queue}, message_id={body.get('message_id')}. Check error: {e}"
            )
            success = False
        finally:
            await rabbitmq_conn.close()
            return success
