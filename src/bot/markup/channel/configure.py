from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.bot.callbacks.channel import ChannelListCallbacks, ChannelConfigCallbacks
from src.core.orm.schemas.channel_config import ChannelConfigResponseSchema


def configure_kb(
        config: ChannelConfigResponseSchema,
        page: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    is_post_owner_report_enabled_button = InlineKeyboardButton(
        text="✅ Report post owner" if not config.is_post_owner_report_enabled else "❌ Report post owner",
        callback_data=ChannelConfigCallbacks.ToggleReportPostOwner(
            channel_id=str(config.channel_id)
        ).pack()
    )

    back_button = InlineKeyboardButton(
        text="Back",
        callback_data=ChannelListCallbacks.ChannelPage(page=page).pack()
    )
    builder.row(is_post_owner_report_enabled_button, back_button)
    builder.adjust(1)
    return builder.as_markup()
