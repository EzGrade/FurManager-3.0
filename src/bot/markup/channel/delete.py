from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.bot.callbacks.channel import ChannelDeleteCallbacks
from src.bot.callbacks.channel import ChannelListCallbacks


def confirm_deletion_kb(channel_id: str, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Yes",
            callback_data=ChannelDeleteCallbacks.ConfirmDeleteChannel(
                channel_id=channel_id
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="No",
            callback_data=ChannelListCallbacks.ChannelPage(page=page).pack()
        )
    )
    return builder.as_markup()
