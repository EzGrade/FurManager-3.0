from dishka import Provider, Scope, provide
from aiogram import Bot

from src.config.bot import BotConfig


class BotProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_bot(self) -> Bot:
        """Provides an instance of the Bot."""
        config = BotConfig()
        return Bot(token=config.TOKEN, validate_token=True)
