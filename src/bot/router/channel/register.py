from dishka import FromDishka
from aiogram import Router, types, Bot
from aiogram.filters import Command, Filter, StateFilter
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import inject

from src.core.orm.handlers.channel import GetOneChannelHandler, CreateChannelHandler
from src.core.models.channel.entity import ChannelModel
from src.core.orm.schemas.channel import ChannelCreateSchema
from src.utils.enums.router.commands import ChanngelCommands
from src.utils.enums.router.states import RegisterChannelStates
from src.utils.exceptions.database.orm import NoRecordsFoundException
from src.utils.tools.bot import is_bot_admin

register_router = Router()


@register_router.message(Command(ChanngelCommands.REGISTER_CHANNEL))
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
    is_admin = await is_bot_admin(
        bot=bot,
        chat_id=int(message.text)
    )
    if not is_admin:
        await message.answer("Bot is not an admin in this chat.")
        return

    try:
        await get_one.handle(telegram_id=int(message.text))
        await message.answer("Channel already registered.")
        return
    except NoRecordsFoundException:
        pass

    await create_one.handle(
        create_model=ChannelCreateSchema(
            name=message.chat.username,
            telegram_id=int(message.text),
            owner_id=message.from_user.id,
        )
    )

    await message.answer("Channel registered successfully.")
    await state.clear()
