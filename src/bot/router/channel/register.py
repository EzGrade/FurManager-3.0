from aiogram import Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatFullInfo
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.core.orm.handlers.channel import GetOneChannelHandler, CreateChannelHandler
from src.core.orm.handlers.user import GetOneUserHandler
from src.core.orm.schemas.channel import ChannelCreateSchema
from src.core.repositories.redis.bot.channels import ChannelsRedisRepository
from src.utils.enums.router.commands import ChannelCommands
from src.utils.enums.router.states import RegisterChannelStates
from src.utils.tools.bot import is_bot_admin, get_chat

register_router = Router()


@register_router.message(Command(ChannelCommands.REGISTER_CHANNEL))
async def register_channel(message: types.Message, state: FSMContext):
    """
    Handler for the /register_channel command.
    """
    await message.answer("Please, forward a message from the channel you want to register")
    await state.set_state(RegisterChannelStates.WAITING_FOR_CHANNEL_ID)


@register_router.message(StateFilter(RegisterChannelStates.WAITING_FOR_CHANNEL_ID))
@inject
async def receive_channel_id(
        message: types.Message,
        state: FSMContext,
        get_one: FromDishka[GetOneChannelHandler],
        get_user: FromDishka[GetOneUserHandler],
        create_one: FromDishka[CreateChannelHandler],
        channels_redis: FromDishka[ChannelsRedisRepository],
        bot: FromDishka[Bot],
):
    """
    Handler for receiving the channel ID.
    This function is triggered when the user sends a channel ID.
    """
    source = message.forward_origin.type
    if source == "channel":
        channel_id = message.forward_origin.chat.id
    else:
        await message.answer(
            f"Please forward a message from the channel you want to register\\. "
            f"Message source is {source}"
        )
        return

    chat: ChatFullInfo = await get_chat(bot=bot, chat_id=channel_id)
    is_admin = await is_bot_admin(bot=bot, chat_id=channel_id)
    if not is_admin:
        await message.answer("Bot is not an admin in this chat")
        return

    channel = await get_one.handle(telegram_id=chat.id)

    if channel:
        await message.answer("Channel already registered")

    if not message.from_user:
        await message.answer("User information is missing")
        return

    owner = await get_user.handle(telegram_id=message.from_user.id)

    await create_one.handle(
        create_model=ChannelCreateSchema(
            name=chat.username,
            title=chat.title,
            telegram_id=chat.id,
            owner_id=owner.uuid,
        )
    )

    await channels_redis.delete_list(
        key=str(owner.uuid)
    )

    await message.answer("Channel registered successfully")
    await state.clear()
