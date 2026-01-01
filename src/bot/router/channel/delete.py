from aiogram import Router, types
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.bot.callbacks.channel import ChannelDeleteCallbacks
from src.bot.markup.channel.delete import confirm_deletion_kb
from src.bot.markup.channel.paginator import back_to_paginator
from src.core.orm.handlers.channel import DeleteChannelHandler, GetOneChannelHandler
from src.core.orm.handlers.user import GetOneUserHandler
from src.core.repositories.redis.bot.channels import ChannelsRedisRepository

delete_router = Router()


@delete_router.callback_query(ChannelDeleteCallbacks.DeleteChannel.filter())
@inject
async def delete_channel(
        callback_query: types.CallbackQuery,
        callback_data: ChannelDeleteCallbacks.DeleteChannel,
):
    kb = confirm_deletion_kb(
        channel_id=callback_data.channel_id,
        page=callback_data.page
    )
    await callback_query.message.edit_text(
        text="Are you sure you want to delete this channel?",
        reply_markup=kb
    )


@delete_router.callback_query(ChannelDeleteCallbacks.ConfirmDeleteChannel.filter())
@inject
async def confirm_delete_channel(
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
        f"Channel deleted successfully",
        reply_markup=back_to_paginator()
    )
