from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from dishka.integrations.aiogram import setup_dishka
from loguru import logger
from redis.asyncio import Redis

from src.bot.di.bot import BotProvider
from src.config.bot import BotConfig
from src.config.redis import RedisConfig
from src.core.di.orm.handlers.channel import ChannelProvider
from src.core.di.orm.handlers.channel_config import ChannelConfigProvider
from src.core.di.orm.handlers.user import UserProvider
from src.core.di.repositories.base import RedisProvider
from src.core.di.repositories.redis.bot import ChannelsRedisRepositoryProvider

config = BotConfig()
logger.info(f"Bot started with token: {config.truncated_token}")


def register_handlers(container, dp: Dispatcher) -> None:
    from src.bot.router.common.basic import basic_router
    from src.bot.router.image.receive import receive_router
    from src.bot.router.channel.register import register_router
    from src.bot.router.channel.list import list_router

    handlers = [
        basic_router,
        receive_router,
        register_router,
        list_router,
    ]
    for handler in handlers:
        dp.include_router(handler)
        setup_dishka(container=container, router=handler)

    logger.info(f"Registered {len(handlers)} router(s).")


async def start_pooling(dp: Dispatcher, bot: Bot):
    await dp.start_polling(bot)


def get_container():
    from dishka import make_async_container

    return make_async_container(
        BotProvider(),
        ChannelProvider(),
        ChannelConfigProvider(),
        UserProvider(),
        RedisProvider(),
        ChannelsRedisRepositoryProvider()
    )


async def main() -> None:
    container = get_container()
    bot = await container.get(Bot)

    redis_config = RedisConfig()
    redis_client = Redis.from_url(
        redis_config.url,
        max_connections=redis_config.POOL_SIZE,
        socket_connect_timeout=redis_config.TIMEOUT,
    )

    try:
        await redis_client.ping()
        logger.opt(colors=True).info("<green>Redis connection successful.</green>")
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        raise e

    storage = RedisStorage(redis=redis_client)
    dp = Dispatcher(storage=storage)

    setup_dishka(container=container, router=dp)
    register_handlers(container, dp=dp)
    if True:
        logger.opt(colors=True).info(
            f"Starting bot polling. Username: <yellow>@{(await bot.get_me()).username}</yellow>"
        )
        logger.info("Press Ctrl+C to stop.")
        await start_pooling(dp, bot)
    else:
        logger.info("Webhook setup is not implemented yet.")


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
