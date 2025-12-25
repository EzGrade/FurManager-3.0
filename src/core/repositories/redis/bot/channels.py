from src.core.orm.schemas.channel import ChannelResponseSchema
from src.core.repositories.base import ListAbstractRepository


class ChannelsRedisRepository(ListAbstractRepository[ChannelResponseSchema]):
    __model__ = ChannelResponseSchema
    __prefix__ = "channels"

    async def append_values(
            self, key: str, values: list[ChannelResponseSchema], ex: int | None = 60 * 60 * 2
    ) -> int:
        return await super().append_values(
            key=key, values=values, ex=ex
        )
