from aiogram import Bot
from aiogram.types import ChatFullInfo

from loguru import logger


async def is_bot_admin(bot: Bot, chat_id: int | str) -> bool:
    """Checks if a user is an admin in a specific chat."""
    try:
        chat = await bot.get_chat(chat_id)
        chat_member = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
        return chat_member.status in (
            "administrator",
            "creator",
        )
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False


async def get_chat(bot: Bot, chat_id: str | int) -> ChatFullInfo | str:
    """Retrieves the name of a chat by its ID."""
    try:
        chat = await bot.get_chat(chat_id)
        return chat
    except Exception as e:
        logger.error(f"Error retrieving chat name: {e}")
        return "Unknown Chat"
