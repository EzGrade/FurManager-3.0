from aiogram import Router, types
from aiogram.filters import Command
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.core.orm.handlers.channel import GetAllChannelsHandler
from src.utils.enums.router.commands import ChannelCommands

list_router = Router()


@list_router.message(Command(ChannelCommands.MY_CHANNELS))
@inject
async def list_channels(
    message: types.Message, get_all: FromDishka[GetAllChannelsHandler]
):
    """
    Handler for the /my_channels command.
    This function is triggered when a user sends the /my_channels command.
    It sends a message listing the user's channels.
    """
    text = "Here are your registered channels:\n\n"

    if not message.from_user:
        await message.answer("User information is missing.")
        return

    channels = await get_all.handle(owner_id=message.from_user.id)

    if not channels:
        await message.answer("You have no registered channels.")
        return

    for channel in channels:
        text += f"- {channel.name} (ID: {channel.telegram_id})\n"

    await message.answer(text)
