from aiogram.filters.callback_data import CallbackData


class BasicCallbacks:
    class DummyCallback(CallbackData, prefix="dummy_callback"):
        pass
