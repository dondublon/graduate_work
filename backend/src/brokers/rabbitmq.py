from aio_pika import connect_robust


class RabbitmqConnection:
    def __init__(self, host):
        self.host = host
        self.conn_sting = f"amqp://guest:guest@{self.host}/"

    async def init_rabbitmq_connection(self):
        connection = await connect_robust(self.conn_sting)
        return connection
