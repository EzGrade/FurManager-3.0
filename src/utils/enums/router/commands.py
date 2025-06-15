from enum import StrEnum


class BasicCommands(StrEnum):
    """Basic commands for the bot."""

    START = "start"
    HELP = "/help"


class ChanngelCommands(StrEnum):
    """Channel commands for the bot."""

    REGISTER_CHANNEL = "register_channel"
