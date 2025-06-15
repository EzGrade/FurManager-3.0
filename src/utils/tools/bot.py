from aiogram import Bot

from loguru import logger


async def is_bot_admin(
        bot: Bot, chat_id: int
) -> bool:
    """Checks if a user is an admin in a specific chat."""
    try:
        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        print(chat_member)
        return chat_member.status in (
            "administrator",
            "creator",
        )
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False
