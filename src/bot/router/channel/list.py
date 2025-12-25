from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from orjson import dumps, loads, OPT_SERIALIZE_UUID

from src.bot.callbacks.channel import ChannelListCallbacks
from src.bot.markup.channel.paginator import paginator_channel_kb
from src.core.orm.handlers.channel import GetAllChannelsHandler
from src.core.orm.handlers.user import GetOneUserHandler
from src.core.orm.schemas.channel import ChannelResponseSchema
from src.utils.enums.router.commands import ChannelCommands

list_router = Router()


async def list_channels_handler(
        message: types.Message | types.CallbackQuery,
        get_user: GetOneUserHandler,
        get_all: GetAllChannelsHandler,
        state: FSMContext,
        page: int = 0,
) -> tuple[str, types.InlineKeyboardMarkup | None] | None:
    if not message.from_user:
        return "User information is missing", None

    await state.set_data({"page": page})

    user = await get_user.handle(telegram_id=message.from_user.id)
    if not user:
        return "Something went wrong\\.\\.\\.", None

    data = await state.get_data()

    if not data.get("channels"):
        channels = await get_all.handle(owner_id=user.uuid)
        channels_json = dumps(
            [channel.model_dump(mode="json") for channel in channels],
            option=OPT_SERIALIZE_UUID,
        ).decode("utf-8")
        await state.update_data(channels=channels_json)
        data = await state.get_data()

    channels_raw = data.get("channels", "[]")
    if isinstance(channels_raw, str):
        channels_payload = loads(channels_raw)
    else:
        channels_payload = channels_raw

    channels = [
        ChannelResponseSchema.model_validate(channel)
        for channel in channels_payload
    ]

    channel_text = channels[page].format()
    keyboard = paginator_channel_kb(page, len(channels))

    if not channels:
        return "You have no registered channels", None

    return channel_text, keyboard


@list_router.message(Command(ChannelCommands.MY_CHANNELS))
@inject
async def list_channels(
        message: types.Message,
        get_user: FromDishka[GetOneUserHandler],
        get_all: FromDishka[GetAllChannelsHandler],
        state: FSMContext,
):
    """
    Handler for the /my_channels command.
    This function is triggered when a user sends the /my_channels command.
    It sends a message listing the user's channels.
    """
    message_text, kb = await list_channels_handler(
        message=message,
        get_user=get_user,
        get_all=get_all,
        state=state
    )
    await message.answer(message_text, reply_markup=kb)


@list_router.callback_query(ChannelListCallbacks.ChannelPage.filter())
@inject
async def configure_channel(
        callback_query: types.CallbackQuery,
        callback_data: ChannelListCallbacks.ChannelPage,
        get_user: FromDishka[GetOneUserHandler],
        get_all: FromDishka[GetAllChannelsHandler],
        state: FSMContext,
):
    await callback_query.answer()
    data = await state.get_data()

    if callback_data.page == data.get("page"):
        return

    message_text, kb = await list_channels_handler(
        message=callback_query,
        get_user=get_user,
        get_all=get_all,
        state=state,
        page=callback_data.page
    )

    await callback_query.message.edit_text(message_text, reply_markup=kb)
