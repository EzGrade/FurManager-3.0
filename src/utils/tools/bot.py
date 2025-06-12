async def get_bot_username() -> str:
    """Retrieve the bot's username."""
    from aiogram import Bot

    bot = Bot.get_current()
    return (await bot.get_me()).username
