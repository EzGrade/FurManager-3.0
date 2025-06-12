from typing import Coroutine

from aiogram import Bot, Dispatcher
from loguru import logger

from config.bot import BotConfig

config = BotConfig()

logger.info(f"Bot started with token: {config.truncated_token}")

bot = Bot(token=BotConfig().TOKEN)
dp = Dispatcher()


def register_handlers() -> None:
    from router.common.basic import basic_router

    handlers = [
        basic_router,
    ]
    dp.include_router(*handlers)
    logger.info(f"Registered {len(handlers)} router(s).")


def start_pooling() -> Coroutine[None, None, None]:
    return dp.start_polling(bot)


async def main() -> None:
    register_handlers()
    if True:
        logger.info("Starting bot polling.")
        await start_pooling()
    else:
        # Code for webhook setup can be added here
        logger.info("Webhook setup is not implemented yet.")


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
