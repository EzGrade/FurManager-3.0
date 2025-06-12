from aiogram import Bot

from di.bot import bot_container


async def get_bot_name(bot: Bot = bot_container.get(Bot)) -> str:
    """Fetches the bot's name."""
    me = await bot.get_me()
    return me.username
