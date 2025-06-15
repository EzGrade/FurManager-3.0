from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.enums.router.commands import ChanngelCommands

from utils.enums.router.states import RegisterChannelStates

register_router = Router()


@register_router.message(Command(ChanngelCommands.REGISTER_CHANNEL))
async def register_channel(message: types.Message, state: FSMContext):
    """
    Handler for the /register_channel command.
    """
    await message.answer("Please send me a channel ID.")
    await state.set_state(RegisterChannelStates.WAITING_FOR_CHANNEL_ID)


@register_router.message(RegisterChannelStates.WAITING_FOR_CHANNEL_ID)
async def receive_channel_id(message: types.Message, state: FSMContext):
    """
    Handler for receiving the channel ID.
    This function is triggered when the user sends a channel ID.
    """
