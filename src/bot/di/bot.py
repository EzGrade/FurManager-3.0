from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dishka import Provider, Scope, provide

from src.config.bot import BotConfig


class BotProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_bot(self) -> Bot:
        """Provides an instance of the Bot."""
        config = BotConfig()
        properties = DefaultBotProperties(parse_mode="MarkdownV2")
        return Bot(token=config.TOKEN, validate_token=True, default=properties)
