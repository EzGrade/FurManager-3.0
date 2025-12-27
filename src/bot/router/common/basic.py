from aiogram import Router, types
from aiogram.filters import Command
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from loguru import logger

from src.bot.callbacks.common import BasicCallbacks
from src.core.orm.handlers.user import (
    GetOneUserHandler,
    CreateUserHandler
)
from src.core.orm.schemas.user import UserCreateSchema
from src.utils.enums.router.commands import BasicCommands

basic_router = Router()


@basic_router.message(Command(BasicCommands.START))
@inject
async def start_command(
        message: types.Message,
        get_one: FromDishka[GetOneUserHandler],
        create_one: FromDishka[CreateUserHandler],
) -> None:
    """Handle the /start command."""

    user = await get_one.handle(telegram_id=message.from_user.id)
    if not user:
        user_obj = UserCreateSchema(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
        await create_one.handle(
            create_model=user_obj
        )
        logger.info(f"User {user_obj.telegram_id} created")

    await message.answer(
        "Hello\\! Welcome to channel management bot"
    )


@basic_router.callback_query(BasicCallbacks.DummyCallback.filter())
async def dummy_callback(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()
