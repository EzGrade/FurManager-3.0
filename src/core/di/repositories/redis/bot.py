from dishka import Provider, provide, Scope
from redis.asyncio.client import Redis

from src.core.repositories.redis.bot.channels import ChannelsRedisRepository


class ChannelsRedisRepositoryProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_channels_redis_repository(
            self,
            redis_client: Redis
    ) -> ChannelsRedisRepository:
        return ChannelsRedisRepository(
            redis_client=redis_client
        )
