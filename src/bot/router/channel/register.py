from aiogram.types import ChatFullInfo
from dishka import FromDishka
from aiogram import Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import inject

from src.core.orm.handlers.channel import GetOneChannelHandler, CreateChannelHandler
from src.core.orm.schemas.channel import ChannelCreateSchema
from src.utils.enums.router.commands import ChannelCommands
from src.utils.enums.router.states import RegisterChannelStates
from src.utils.exceptions.database.orm import NoRecordsFoundException
from src.utils.tools.bot import is_bot_admin, get_chat

register_router = Router()


@register_router.message(Command(ChannelCommands.REGISTER_CHANNEL))
async def register_channel(message: types.Message, state: FSMContext):
    """
    Handler for the /register_channel command.
    """
    await message.answer("Please send me a channel ID.")
    await state.set_state(RegisterChannelStates.WAITING_FOR_CHANNEL_ID)


@register_router.message(StateFilter(RegisterChannelStates.WAITING_FOR_CHANNEL_ID))
@inject
async def receive_channel_id(
        message: types.Message,
        state: FSMContext,
        get_one: FromDishka[GetOneChannelHandler],
        create_one: FromDishka[CreateChannelHandler],
        bot: FromDishka[Bot],
):
    """
    Handler for receiving the channel ID.
    This function is triggered when the user sends a channel ID.
    """
    channel_id = message.text.strip() if message.text else ""
    chat: ChatFullInfo = await get_chat(bot=bot, chat_id=channel_id)

    is_admin = await is_bot_admin(bot=bot, chat_id=channel_id)
    if not is_admin:
        await message.answer("Bot is not an admin in this chat.")
        return

    try:
        await get_one.handle(telegram_id=chat.id)
        await message.answer("Channel already registered.")
        return
    except NoRecordsFoundException:
        pass

    if not message.from_user:
        await message.answer("User information is missing.")
        return

    await create_one.handle(
        create_model=ChannelCreateSchema(
            name=chat.username,
            title=chat.title,
            telegram_id=chat.id,
            owner_id=message.from_user.id,
        )
    )

    await message.answer("Channel registered successfully.")
    await state.clear()
