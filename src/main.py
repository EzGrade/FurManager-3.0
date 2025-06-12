from typing import Coroutine

from aiogram import Dispatcher, Bot
from loguru import logger

from di.bot import bot_container
from config.bot import BotConfig
from utils.tools.bot import get_bot_name

config = BotConfig()
logger.info(f"Bot started with token: {config.truncated_token}")

dp = Dispatcher()


def register_handlers() -> None:
    from router.common.basic import basic_router

    handlers = [
        basic_router,
    ]
    dp.include_router(*handlers)
    logger.info(f"Registered {len(handlers)} router(s).")


def start_pooling() -> Coroutine[None, None, None]:
    return dp.start_polling(bot_container.get(Bot))


async def main() -> None:
    register_handlers()
    if True:
        logger.info(f"Starting bot polling. Username: {await get_bot_name()}")
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
