from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton
)

from src.bot.callbacks.channel import (
    ChannelListCallbacks,
    ChannelDeleteCallbacks,
    ChannelConfigCallbacks
)
from src.bot.markup.common.paginator import paginator_inline_kb


def paginator_channel_kb(
        page: int,
        total_pages: int,
        channel_id: str
) -> InlineKeyboardMarkup:
    paginator = paginator_inline_kb(page, total_pages, ChannelListCallbacks.ChannelPage)
    configure_button = InlineKeyboardButton(
        text="Configure",
        callback_data=ChannelConfigCallbacks.ConfigureChannel(channel_id=channel_id).pack()
    )
    delete_button = InlineKeyboardButton(
        text="Delete",
        callback_data=ChannelDeleteCallbacks.DeleteChannel(channel_id=channel_id).pack()
    )

    builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [configure_button, delete_button]
    buttons.extend([button for button in paginator.buttons])
    builder.row(*buttons)
    builder.adjust(2, 3)
    return builder.as_markup()
