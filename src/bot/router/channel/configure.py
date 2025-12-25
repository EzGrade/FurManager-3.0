from aiogram import Router, types
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.bot.callbacks.channel import ChannelConfigCallbacks
from src.core.orm.handlers.channel import GetOneChannelHandler
from src.core.orm.handlers.channel_config import GetOneChannelConfigHandler
from src.core.orm.handlers.user import GetOneUserHandler

config_router = Router()


@config_router.callback_query(ChannelConfigCallbacks.ConfigureChannel.filter())
@inject
async def delete_channel(
        callback_query: types.CallbackQuery,
        get_user: FromDishka[GetOneUserHandler],
        get_channel: FromDishka[GetOneChannelHandler],
        get_config: FromDishka[GetOneChannelConfigHandler],
        callback_data: ChannelConfigCallbacks.ConfigureChannel
):
    channel_id = callback_data.channel_id
    user = await get_user.handle(telegram_id=callback_query.from_user.id)

    if not user:
        await callback_query.message.answer("Something went wrong")

    channel = await get_channel.handle(uuid=channel_id, owner_id=user.uuid)
    if not channel:
        await callback_query.message.answer(
            f"Channel is not registered by you"
        )

    config = await get_config.handle(channel_id=channel_id)
    text = config.format(user=user)
    await callback_query.message.edit_text(
        text=text
    )
