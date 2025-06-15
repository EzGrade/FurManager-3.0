from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

receive_router = Router()


@receive_router.message(Command("send_image"))
async def receive_image(message: types.Message, state: FSMContext):
    """
    Handler for the /send_image command.
    This function is triggered when a user sends the /send_image command.
    It sends a message prompting the user to send an image.
    """
    await message.answer("Please send me an image.")
    await state.set_state("waiting_for_image")
