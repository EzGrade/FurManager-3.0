from dishka import Provider, Scope, provide

from src.config.database import PostgresConfig
from src.core.orm.core import Database
from src.core.orm.handlers.channel_config import (
    GetAllChannelConfigsHandler,
    GetOneChannelConfigHandler,
    CreateChannelConfigHandler,
    UpdateChannelConfigHandler,
    DeleteChannelConfigHandler,
)
from src.core.repositories.orm.channel_config import ChannelConfigRepository
from src.core.services.database.channel_config import ChannelConfigServiceConfig, ChannelConfigService
from src.utils.interfaces.database.unit_of_work import UnitOfWork


class ChannelConfigProvider(Provider):
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
    def provide_channel_repository(self) -> ChannelConfigRepository:
        """Provides an instance of the ChannelConfigRepository."""
        return ChannelConfigRepository()

    @provide(scope=Scope.REQUEST)
    def provide_channel_config_service(
            self, channel_repository: ChannelConfigRepository
    ) -> ChannelConfigService:
        """Provides an instance of the ChannelConfigService."""
        config = ChannelConfigServiceConfig(channel_config_repository=channel_repository)
        return ChannelConfigService(config=config)

    @provide(scope=Scope.REQUEST)
    def provide_get_all_channels_handler(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> GetAllChannelConfigsHandler:
        """Provides an instance of the GetAllChannelConfigsHandler."""
        return GetAllChannelConfigsHandler(
            channel_config_service=channel_config_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_one_channel_handler(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> GetOneChannelConfigHandler:
        """Provides an instance of the GetOneChannelConfigHandler."""
        return GetOneChannelConfigHandler(
            channel_config_service=channel_config_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_create_channel_handler(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> CreateChannelConfigHandler:
        """Provides an instance of the CreateChannelConfigHandler."""
        return CreateChannelConfigHandler(
            channel_config_service=channel_config_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_update_channel_handler(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> UpdateChannelConfigHandler:
        """Provides an instance of the UpdateChannelConfigHandler."""
        return UpdateChannelConfigHandler(
            channel_config_service=channel_config_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_delete_channel_handler(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> DeleteChannelConfigHandler:
        """Provides an instance of the DeleteChannelConfigHandler."""
        return DeleteChannelConfigHandler(
            channel_config_service=channel_config_service, unit_of_work=unit_of_work
        )
