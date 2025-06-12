from typing import Coroutine

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from redis import Redis
from loguru import logger

from di.bot import bot_container
from config.bot import BotConfig
from di.redis import redis_container
from utils.tools.bot import get_bot_name

config = BotConfig()
logger.info(f"Bot started with token: {config.truncated_token}")

storage = RedisStorage(redis=redis_container.get(Redis))
dp = Dispatcher(storage=storage)


def register_handlers() -> None:
    from router.common.basic import basic_router
    from router.image.receive import receive_router

    handlers = [
        basic_router,
        receive_router,
    ]
    dp.include_routers(*handlers)
    logger.info(f"Registered {len(handlers)} router(s).")


def start_pooling() -> Coroutine[None, None, None]:
    return dp.start_polling(bot_container.get(Bot))


async def main() -> None:
    register_handlers()
    if True:
        logger.opt(colors=True).info(f"Starting bot polling. Username: <yellow>@{await get_bot_name()}</yellow>")
        logger.info("Press Ctrl+C to stop.")
        await start_pooling()
    else:
        logger.info("Webhook setup is not implemented yet.")


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
