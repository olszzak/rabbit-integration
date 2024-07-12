from typing import Callable
import json
from aio_pika import ExchangeType, connect, Message
from aio_pika.abc import AbstractConnection

from messages.schema import BaseMessageSchema


class RabbitClient:
    def __init__(self, connection: AbstractConnection):
        self._con = connection

    async def consume(self, queue: str, on_message_method: Callable) -> None:
        channel = await self._con.channel()
        await channel.set_qos(prefetch_count=1)

        exchange = await channel.declare_exchange(
            queue,
            ExchangeType.DIRECT,
        )

        queue = await channel.declare_queue(queue, durable=True)

        await queue.bind(exchange)

        await queue.consume(on_message_method)

    async def send(self, queue: str, message_data: BaseMessageSchema) -> None:
        channel = await self._con.channel()
        exchange = await channel.declare_exchange(
            queue,
            ExchangeType.DIRECT,
        )

        queue = await channel.declare_queue(queue, durable=True)

        message_body = message_data.model_dump()

        message = Message(body=json.dumps(message_body).encode())

        await exchange.publish(
            message,
            routing_key=queue.name,
        )


async def get_rabbit_client(
    user: str, password: str, host: str, port: int
) -> RabbitClient:
    connection = await connect(f"amqp://{user}:{password}@{host}:{port}/")
    return RabbitClient(connection)
