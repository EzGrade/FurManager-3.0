from aiogram.filters.callback_data import CallbackData


class ChannelListCallbacks:
    class ChannelPage(CallbackData, prefix="channel_page"):
        page: int


class ChannelDeleteCallbacks:
    class DeleteChannel(CallbackData, prefix="delete_channel"):
        channel_id: str


class ChannelConfigCallbacks:
    class ConfigureChannel(CallbackData, prefix="configure_channel"):
        channel_id: str

    class ToggleReportPostOwner(CallbackData, prefix="toggle_report_post_owner"):
        channel_id: str
