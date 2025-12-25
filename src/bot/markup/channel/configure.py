from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.bot.callbacks.channel import ChannelListCallbacks


def configure_kb(page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    back_button = InlineKeyboardButton(
        text="Back",
        callback_data=ChannelListCallbacks.ChannelPage(page=page).pack()
    )
    builder.row(back_button)
    return builder.as_markup()
