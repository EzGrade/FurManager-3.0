from aiogram import Bot

from loguru import logger

from bot.di.bot import bot_container


async def get_bot_name(bot: Bot = bot_container.get(Bot)) -> str:
    """Fetches the bot's name."""
    me = await bot.get_me()
    if not me.username:
        logger.error("Bot username is not set.")
        raise
    return me.username
