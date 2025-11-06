import json
import pickle
from dataclasses import dataclass

from redis.asyncio import ConnectionPool, Redis

from infrastructure.config.redis import RedisConfig


@dataclass
class BaseAsyncCache:
    redis_pool: ConnectionPool
    config: RedisConfig

    serialization: str = 'pickle'

    @property
    def serializer(self):
        return dict(
            pickle=pickle.dumps,
            json=json.dumps
        ).get(self.serialization)

    @property
    def deserializer(self):
        return dict(
            pickle=pickle.loads,
            json=json.loads
        ).get(self.serialization)

    def get_connection(self):
        return Redis(
            host=self.config.host,
            port=self.config.port,
            connection_pool=self.redis_pool,
        )

    def serialize(self, resp) -> bytes:
        return self.serializer(resp)

    def deserialize(self, data: bytes):
        return self.deserializer(data) if data else None


class DomainCache(BaseAsyncCache):
    key = None

    async def load(self, objs: list):
        async with self.get_connection() as conn:
            await conn.set(self.key, self.serialize(objs))

    async def get(self) -> list:
        async with self.get_connection() as conn:
            raw_objs = await conn.get(self.key)
            if raw_objs:
                return self.deserialize(raw_objs)

    async def clear(self):
        async with self.get_connection() as conn:
            await conn.delete(self.key)
