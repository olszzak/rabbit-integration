from fastapi import Depends

from messages.rabbit_client import RabbitClient, get_rabbit_client
from settings import get_settings

settings = get_settings()


class GetRabbitClient:
    async def __call__(self) -> RabbitClient:
        return await get_rabbit_client(**settings.RABBIT_CONFIG.model_dump())


GetRabbitClientDependency = Depends(GetRabbitClient())
