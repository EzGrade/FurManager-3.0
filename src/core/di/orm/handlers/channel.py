from dishka import make_container, Provider, Scope

from src.config.database import PostgresConfig
from src.utils.interfaces.database.unit_of_work import UnitOfWork
from src.core.services.database.channel import ChannelServiceConfig, ChannelService
from src.core.repositories.orm.channel import ChannelRepository
from src.core.orm.handlers.channel import (
    GetAllChannelsHandler
)
from src.core.orm.core import Database

channel_provider = Provider(scope=Scope.REQUEST)
channel_container = make_container(channel_provider)


@channel_provider.provide
def provide_unit_of_work() -> UnitOfWork:
    """Provides an instance of the UnitOfWork."""
    pg_config = PostgresConfig()
    database = Database(
        db_url=pg_config.async_db_uri,
    )
    return UnitOfWork(
        async_session_factory=database.async_session_maker,
    )


@channel_provider.provide
def provide_channel_repository() -> ChannelRepository:
    """Provides an instance of the ChannelRepository."""
    return ChannelRepository()


@channel_provider.provide
def provide_channel_service() -> ChannelService:
    """Provides an instance of the ChannelService."""
    config = ChannelServiceConfig(channel_repository=channel_container.get(ChannelRepository))
    return ChannelService(config=config)


@channel_provider.provide
def provide_get_all_channels_handler() -> GetAllChannelsHandler:
    """Provides an instance of the GetAllChannelsHandler."""

    channel_service = channel_container.get(ChannelService)
    uof = channel_container.get(UnitOfWork)
    return GetAllChannelsHandler(channel_service=channel_service, unit_of_work=uof)
