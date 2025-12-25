from dishka import Provider, provide, Scope
from redis.asyncio.client import Redis

from src.config.redis import RedisConfig


class RedisProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_redis_config(self) -> RedisConfig:
        return RedisConfig()

    @provide(scope=Scope.APP)
    def provide_redis(self) -> Redis:
        config: RedisConfig = self.provide_redis_config()
        return Redis(
            host=config.HOST,
            port=config.PORT,
            db=config.DB,
            password=config.PASSWORD,
            decode_responses=True,
        )
