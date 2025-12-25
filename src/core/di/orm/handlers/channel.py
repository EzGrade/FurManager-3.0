from dishka import Provider, Scope, provide

from src.config.database import PostgresConfig
from src.core.orm.core import Database
from src.core.orm.handlers.channel import (
    GetAllChannelsHandler,
    GetOneChannelHandler,
    CreateChannelHandler,
    UpdateChannelHandler,
    DeleteChannelHandler,
)
from src.core.repositories.orm.channel import ChannelRepository
from src.core.services.database.channel import ChannelServiceConfig, ChannelService
from src.core.services.database.channel_config import ChannelConfigService
from src.utils.interfaces.database.unit_of_work import UnitOfWork


class ChannelProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_unit_of_work(self) -> UnitOfWork:
        """Provides an instance of the UnitOfWork."""
        pg_config = PostgresConfig()
        database = Database(
            db_url=pg_config.async_db_uri,
        )
        return UnitOfWork(
            async_session_factory=database.async_session_maker,
        )

    @provide(scope=Scope.REQUEST)
    def provide_channel_repository(self) -> ChannelRepository:
        """Provides an instance of the ChannelRepository."""
        return ChannelRepository()

    @provide(scope=Scope.REQUEST)
    def provide_channel_service(
            self, channel_repository: ChannelRepository
    ) -> ChannelService:
        """Provides an instance of the ChannelService."""
        config = ChannelServiceConfig(channel_repository=channel_repository)
        return ChannelService(config=config)

    @provide(scope=Scope.REQUEST)
    def provide_get_all_channels_handler(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> GetAllChannelsHandler:
        """Provides an instance of the GetAllChannelsHandler."""
        return GetAllChannelsHandler(
            channel_service=channel_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_one_channel_handler(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> GetOneChannelHandler:
        """Provides an instance of the GetOneChannelHandler."""
        return GetOneChannelHandler(
            channel_service=channel_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_create_channel_handler(
            self,
            channel_service: ChannelService,
            channel_config_service: ChannelConfigService,
            unit_of_work: UnitOfWork
    ) -> CreateChannelHandler:
        """Provides an instance of the CreateChannelHandler."""
        return CreateChannelHandler(
            channel_config_service=channel_config_service,
            channel_service=channel_service,
            unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_update_channel_handler(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> UpdateChannelHandler:
        """Provides an instance of the UpdateChannelHandler."""
        return UpdateChannelHandler(
            channel_service=channel_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_delete_channel_handler(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> DeleteChannelHandler:
        """Provides an instance of the DeleteChannelHandler."""
        return DeleteChannelHandler(
            channel_service=channel_service, unit_of_work=unit_of_work
        )
