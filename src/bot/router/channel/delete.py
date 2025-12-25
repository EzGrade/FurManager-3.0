from aiogram import Router, types
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.bot.callbacks.channel import ChannelDeleteCallbacks
from src.core.orm.handlers.channel import DeleteChannelHandler, GetOneChannelHandler
from src.core.orm.handlers.user import GetOneUserHandler
from src.core.repositories.redis.bot.channels import ChannelsRedisRepository

delete_router = Router()


@delete_router.callback_query(ChannelDeleteCallbacks.DeleteChannel.filter())
@inject
async def delete_channel(
        callback_query: types.CallbackQuery,
        get_user: FromDishka[GetOneUserHandler],
        get_channel: FromDishka[GetOneChannelHandler],
        delete_one: FromDishka[DeleteChannelHandler],
        channels_redis: FromDishka[ChannelsRedisRepository],
        callback_data: ChannelDeleteCallbacks.DeleteChannel
):
    channel_id = callback_data.channel_id
    user = await get_user.handle(telegram_id=callback_query.from_user.id)

    if not user:
        await callback_query.message.answer("Something went wrong")

    channel = await get_channel.handle(uuid=channel_id, owner_id=user.uuid)
    if not channel:
        await callback_query.message.answer(
            f"Channel with id {channel_id} is not registered for you"
        )

    await delete_one.handle(
        uuid=channel.uuid
    )
    await channels_redis.delete_list(key=str(user.uuid))

    await callback_query.message.edit_text(
        f"Channel deleted successfully"
    )
