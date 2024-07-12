import redis.asyncio as redis

from schemas import BaseMessageSchema


class RedisClient:
    def __init__(self, password: str, host: str, port: int):
        self._connection = redis.from_url(f"redis://:{password}@{host}:{port}/0")

    async def add_data(self, data: BaseMessageSchema) -> None:
        await self._connection.set(data.key, data.value)

    async def get_data(self, key: str) -> str:
        return await self._connection.get(key)


async def get_redis_client(password: str, host: str, port: int) -> RedisClient:
    return RedisClient(host=host, port=port, password=password)
