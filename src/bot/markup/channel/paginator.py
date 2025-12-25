from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton
)

from src.bot.callbacks.channel import ChannelListCallbacks
from src.bot.markup.common.paginator import paginator_inline_kb


def paginator_channel_kb(page: int, total_pages: int) -> InlineKeyboardMarkup:
    paginator = paginator_inline_kb(page, total_pages, ChannelListCallbacks.ChannelPage)
    configure_button = InlineKeyboardButton(
        text="Configure Channel",
        callback_data=ChannelListCallbacks.ConfigureChannel(page=page).pack()
    )

    builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [configure_button] + [button for button in paginator.buttons]
    builder.row(*buttons)
    builder.adjust(1, 3)
    return builder.as_markup()
