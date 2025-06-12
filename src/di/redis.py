from dishka import make_container, Provider, Scope
from redis import Redis

from loguru import logger

from config.redis import RedisConfig

redis_provider = Provider(scope=Scope.APP)


@redis_provider.provide
def redis_client() -> Redis:
    config = RedisConfig()
    _redis_client = Redis.from_url(
        config.url,
        max_connections=config.POOL_SIZE,
        socket_connect_timeout=config.TIMEOUT,
    )
    try:
        _redis_client.ping()
        logger.opt(colors=True).info("<green>Redis connection successful.</green>")
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        raise e
    return _redis_client


redis_container = make_container(redis_provider)
