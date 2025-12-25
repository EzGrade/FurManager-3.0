from uuid import UUID

from src.core.orm.filters.channel_config import ChannelConfigFilterModel
from src.core.orm.schemas.channel_config import (
    ChannelConfigResponseSchema,
    ChannelConfigCreateSchema,
    ChannelConfigUpdateSchema,
)
from src.core.orm.sorters.channel_config import ChannelConfigSortValues
from src.core.services.database.channel_config import ChannelConfigService
from src.utils.interfaces.database.unit_of_work import UnitOfWork
from src.utils.interfaces.handler import BaseDatabaseHandler


class GetAllChannelConfigsHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_config_service = channel_config_service

    async def handle(
            self, sort_by: ChannelConfigSortValues | None = None, **kwargs
    ) -> list[ChannelConfigResponseSchema] | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_config_service.get_all(
                    async_session=uow_session, sort_by=sort_by, **kwargs
                )

            return None


class GetOneChannelConfigHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_config_service = channel_config_service

    async def handle(self, **kwargs) -> ChannelConfigResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_config_service.get_one_by_filters(
                    async_session=uow_session, filters=ChannelConfigFilterModel(**kwargs)
                )

            return None


class CreateChannelConfigHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_config_service = channel_config_service

    async def handle(
            self,
            create_model: ChannelConfigCreateSchema,
    ) -> ChannelConfigResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_config_service.create(
                    async_session=uow_session, create_model=create_model
                )

            return None


class UpdateChannelConfigHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_config_service = channel_config_service

    async def handle(
            self,
            update_model: ChannelConfigUpdateSchema,
    ) -> ChannelConfigResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_config_service.update(
                    async_session=uow_session, update_model=update_model
                )

            return None


class DeleteChannelConfigHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_config_service: ChannelConfigService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_config_service = channel_config_service

    async def handle(
            self,
            uuid: UUID,
    ) -> int | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_config_service.delete_one_by_uuid(
                    async_session=uow_session, uuid=uuid
                )

            return None
