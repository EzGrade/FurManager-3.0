from dishka import make_container, Provider, Scope
from aiogram import Bot

from src.config.bot import BotConfig

bot_provider = Provider(scope=Scope.APP)


@bot_provider.provide
def provide_bot() -> Bot:
    """Provides an instance of the Bot."""
    config = BotConfig()
    return Bot(token=config.TOKEN, validate_token=True)


bot_container = make_container(bot_provider)
