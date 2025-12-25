from aiogram.filters.callback_data import CallbackData


class ChannelListCallbacks:
    class ChannelPage(CallbackData, prefix="channel_page"):
        page: int

    class ConfigureChannel(CallbackData, prefix="configure_channel"):
        page: int
