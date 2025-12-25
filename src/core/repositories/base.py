from abc import ABC
from typing import Any, Type, Literal

import orjson
from redis.asyncio.client import Redis

from src.core.models.base import BaseEntityModel
from src.utils.exceptions.base import BaseRepositoryException

type _StrType = str | bytes


class BaseAbstractCacheRepository[AbstractModel: BaseEntityModel](ABC):
    """Base class for else repositories which work with cache"""

    __model__: AbstractModel
    __prefix__: str

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    def _get_key(self, key: str) -> str:
        return f"{self.__prefix__}:{key}"

    def _convert_to_entity_model(self, retrieved: Any) -> AbstractModel:
        if not retrieved:
            raise BaseRepositoryException()

        return self.__model__.model_validate(orjson.loads(retrieved))

    async def _delete_by_key(self, key: str) -> int:
        return await self.redis_client.delete(self._get_key(key))

    async def base_set(self, key: str, value: _StrType, **kwargs) -> bool | None:
        return await self.redis_client.set(self._get_key(key), value, **kwargs)

    async def base_get(self, key: str) -> _StrType | None:
        return await self.redis_client.get(self._get_key(key))

    async def set_expire(self, key: str, expire: int) -> bool:
        return await self.redis_client.expire(self._get_key(key), expire)

    async def _delete_by_keys(self, keys: list[str]) -> int:
        return await self.redis_client.delete(*keys)


class SetAbstractRepository[Value: BaseEntityModel](BaseAbstractCacheRepository[Value]):
    async def add_to_set(self, value: Value, key: str) -> int:
        return await self.redis_client.sadd(self._get_key(key), value.model_dump_json())

    async def set_members(self, key: str) -> list[Value]:
        members = await self.redis_client.smembers(self._get_key(key))

        return [self._convert_to_entity_model(member) for member in members]

    async def delete_set(self, key: str) -> int:
        return await super()._delete_by_key(key)

    async def _delete_element(self, key: str, entity: Value) -> int:
        return await self.redis_client.srem(
            self._get_key(key), entity.model_dump_json()
        )

    async def _exists(self, key: str, entity: Value) -> Literal[0, 1]:
        return await self.redis_client.sismember(
            self._get_key(key), entity.model_dump_json()
        )


class StreamAbstractRepository[AbstractModel: BaseEntityModel](
    BaseAbstractCacheRepository[AbstractModel]
):
    """Base class for else repositories which work with streams"""

    __model__: AbstractModel

    def _convert_to_entity_model(self, retrieved: Any) -> AbstractModel:
        if not retrieved:
            raise BaseRepositoryException()

        return self.__model__.model_validate(retrieved)

    async def _add_to_stream(self, key: str, value: dict) -> int:
        return await self.redis_client.xadd(self._get_key(key), value)

    async def _get_stream(
            self, streams: dict[str, str], count: int, block: int | None = 0
    ) -> list[dict]:
        prefix_streams = {self._get_key(key): value for key, value in streams.items()}
        return await self.redis_client.xread(
            streams=prefix_streams, count=count, block=block
        )


class StringAbstractRepository[AbstractModel: BaseEntityModel](
    BaseAbstractCacheRepository[AbstractModel]
):
    """Base class for work with string data types"""

    __model__: Type = AbstractModel  # type: ignore[misc, assignment]

    async def _set_value(
            self, key: str, value: str, ex: int | None = None, **kwargs
    ) -> bool | None:
        return await self.redis_client.set(self._get_key(key), value, ex=ex, **kwargs)

    async def _get_keys(self, pattern: str) -> list[str]:
        return await self.redis_client.keys(self._get_key(pattern))

    async def _get_content_by_keys(self, keys: list[str]) -> list:
        prefix_keys = [self._get_key(key) for key in keys]
        return await self.redis_client.mget(keys=prefix_keys)

    async def _get(self, key: str) -> str | None:
        return await self.redis_client.get(self._get_key(key))

    async def _append(self, key: str, value: str) -> int:
        return await self.redis_client.append(self._get_key(key), value)


class ListAbstractRepository[AbstractModel: BaseEntityModel](
    BaseAbstractCacheRepository[AbstractModel]
):
    """Base class for work with list"""

    __model__ = AbstractModel  # type: ignore[misc]

    async def retrieve_list(
            self, key: str, start: int | None = 0, end: int | None = -1
    ) -> list[AbstractModel]:
        result = await self.redis_client.lrange(
            name=self._get_key(key),
            start=start,  # type: ignore[arg-type]
            end=end,  # type: ignore[arg-type]
        )

        return [self._convert_to_entity_model(raw_data) for raw_data in result]

    async def append_values(
            self, key: str, values: list[AbstractModel], ex: int | None = None
    ) -> int:
        """
        Appends values to a list by key, if list does exist by key first create it and append to the tail
        Do by pipline for reduce number of network round trips between application and server
        """
        pipeline = self.redis_client.pipeline()

        result = await pipeline.rpush(
            self._get_key(key),
            *[datum.model_dump_json(by_alias=True) for datum in values],
        )

        if ex is not None:
            await pipeline.expire(self._get_key(key), ex)

        await pipeline.execute()
        return result

    async def pop_list(self, key: str) -> list[AbstractModel]:
        """Get and delete list with content"""
        pipeline = self.redis_client.pipeline()

        async with pipeline:
            result = await self.retrieve_list(key=key)
            await self.delete_list(key)

        await pipeline.execute()
        return result

    async def delete_list(self, key: str) -> int:
        return await self._delete_by_key(key)

    async def _delete_element(self, key: str, entity: AbstractModel):
        await self.redis_client.lrem(self._get_key(key), 1, entity.model_dump_json())
