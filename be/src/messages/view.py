import json
import logging
from http import HTTPStatus

from aio_pika.abc import AbstractIncomingMessage
from fastapi import APIRouter

from messages.dependencies import GetRabbitClientDependency
from messages.rabbit_client import RabbitClient
from messages.schema import MessageSchema, DownloadMessageSchema
from settings import get_settings

settings = get_settings()
router = APIRouter(tags=["messages"])


@router.post("/messages", status_code=HTTPStatus.CREATED)
async def create_message(
    payload: MessageSchema, rabbit_client: RabbitClient = GetRabbitClientDependency
):
    await rabbit_client.send(settings.UPLOAD_DATA_QUEUE_NAME, payload)


@router.get("/messages/{key}", response_model=MessageSchema | None)
async def get_message(
    key: str, rabbit_client: RabbitClient = GetRabbitClientDependency
):
    await rabbit_client.send(
        settings.DOWNLOAD_DATA_QUEUE_NAME, DownloadMessageSchema(key=key)
    )

    retrieved_data = None

    async def on_message(message: AbstractIncomingMessage) -> None:
        async with message.process():
            nonlocal retrieved_data
            retrieved_data = MessageSchema(**json.loads(message.body))

    await rabbit_client.consume(
        settings.RETRIEVE_DATA_QUEUE_NAME.substitute(key=key), on_message
    )

    if retrieved_data:
        return retrieved_data
    else:
        return None
