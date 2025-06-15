from aiogram import Router, types
from aiogram.filters import Command

from src.utils.enums.router.commands import BasicCommands

basic_router = Router()


@basic_router.message(Command(BasicCommands.START))
async def start_command(message: types.Message) -> None:
    """Handle the /start command."""
    await message.answer(
        "Welcome via START command in router! How can I assist you today?"
    )
