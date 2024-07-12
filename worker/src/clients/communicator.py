import json
from string import Template

from aio_pika.abc import AbstractIncomingMessage

from clients.rabbit_client import RabbitClient, get_rabbit_client
from clients.redis_client import RedisClient, get_redis_client
from schemas import MessageSchema, DownloadMessageSchema
from settings import get_settings

settings = get_settings()


class Communicator:
    def __init__(
        self,
        rabbit_client: RabbitClient,
        redis_client: RedisClient,
        retrieve_data_queue: Template,
        upload_data_queue: str,
        download_data_queue: str,
    ):
        self._rabbit_client = rabbit_client
        self._redis_client = redis_client

        self._retrieve_data_queue = retrieve_data_queue
        self._upload_data_queue = upload_data_queue
        self._download_data_queue = download_data_queue

    async def on_upload_data(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            payload = json.loads(message.body)
            validated_payload = MessageSchema(**payload)
            await self._redis_client.add_data(validated_payload)

    async def on_download_data(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            payload = json.loads(message.body)
            validated_payload = DownloadMessageSchema(**payload)
            if data := await self._redis_client.get_data(validated_payload.key):
                await self._rabbit_client.send(
                    self._retrieve_data_queue.substitute(key=validated_payload.key),
                    MessageSchema(key=validated_payload.key, value=data),
                )

    async def listen_for_upload_data(self) -> None:
        await self._rabbit_client.consume(self._upload_data_queue, self.on_upload_data)

    async def listen_for_download_data(self) -> None:
        await self._rabbit_client.consume(
            self._download_data_queue, self.on_download_data
        )


async def get_communicator() -> Communicator:
    rabbit_client = await get_rabbit_client(**settings.RABBIT_CONFIG.model_dump())
    redis_client = await get_redis_client(**settings.REDIS_CONFIG.model_dump())

    return Communicator(
        rabbit_client,
        redis_client,
        settings.RETRIEVE_DATA_QUEUE_NAME,
        settings.UPLOAD_DATA_QUEUE_NAME,
        settings.DOWNLOAD_DATA_QUEUE_NAME,
    )
