from aiogram.fsm.state import StatesGroup, State


class RegisterChannelStates(StatesGroup):
    """States for registering a channel."""

    WAITING_FOR_CHANNEL_ID = State()
    CONFIRMATION = State()
    COMPLETED = State()
    ERROR = State()
