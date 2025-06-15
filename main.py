from typing import Coroutine

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from loguru import logger

from src.bot.di.bot import bot_container
from src.config.bot import BotConfig
from src.config.redis import RedisConfig
from src.utils.tools.bot import get_bot_name

config = BotConfig()
logger.info(f"Bot started with token: {config.truncated_token}")


def register_handlers(dp: Dispatcher) -> None:
    from src.bot.router.common.basic import basic_router
    from src.bot.router.image.receive import receive_router
    from src.bot.router.channel.register import register_router

    handlers = [
        basic_router,
        receive_router,
        register_router,
    ]
    dp.include_routers(*handlers)
    logger.info(f"Registered {len(handlers)} router(s).")


def start_pooling(dp: Dispatcher) -> Coroutine[None, None, None]:
    return dp.start_polling(bot_container.get(Bot))


async def main() -> None:
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

    register_handlers(dp)
    if True:
        logger.opt(colors=True).info(
            f"Starting bot polling. Username: <yellow>@{await get_bot_name()}</yellow>"
        )
        logger.info("Press Ctrl+C to stop.")
        await start_pooling(dp)
    else:
        logger.info("Webhook setup is not implemented yet.")


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
