from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import BaseConfig


class BotConfig(BaseConfig):
    TOKEN: str = Field(...)

    model_config = SettingsConfigDict(env_prefix="BOT_")

    @property
    def truncated_token(self) -> str:
        """Returns a truncated version of the bot token for logging."""
        return self.TOKEN[:5] + "..." + self.TOKEN[-5:] if len(self.TOKEN) > 10 else self.TOKEN
