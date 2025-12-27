from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton
)

from src.bot.callbacks.common import BasicCallbacks


def paginator_inline_kb(
        page: int,
        total_pages: int,
        page_callback: type[CallbackData]
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if total_pages < 1:
        return builder

    if total_pages != 1:
        if page > 0:
            left_button = InlineKeyboardButton(
                text="⬅️",
                callback_data=page_callback(page=page - 1).pack()
            )
        else:
            left_button = InlineKeyboardButton(
                text=f"to last",
                callback_data=page_callback(page=total_pages - 1).pack()
            )

        if page == total_pages - 1 and total_pages > 1:
            right_button = InlineKeyboardButton(
                text="to first",
                callback_data=page_callback(page=0).pack()
            )
        else:
            right_button = InlineKeyboardButton(
                text="➡️",
                callback_data=page_callback(page=page + 1).pack()
            )
        buttons.extend([left_button, right_button])

    buttons.insert(
        1,
        InlineKeyboardButton(
            text=f"Page {page + 1}/{total_pages}",
            callback_data=BasicCallbacks.DummyCallback().pack()
        )
    )

    builder.row(*buttons)

    return builder
