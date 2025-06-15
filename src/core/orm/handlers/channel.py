from uuid import UUID

from src.core.orm.filters.channel import ChannelFilterModel
from src.core.orm.schemas.channel import ChannelResponseSchema, ChannelCreateSchema, ChannelUpdateSchema
from src.core.orm.sorters.channel import ChannelSortValues
from src.core.services.database.channel import ChannelService
from src.utils.interfaces.handler import BaseDatabaseHandler
from src.utils.interfaces.database.unit_of_work import UnitOfWork


class GetAllChannelsHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_service = channel_service

    async def handle(
            self, sort_by: ChannelSortValues | None = None, **kwargs
    ) -> list[ChannelResponseSchema] | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_service.get_all(
                    async_session=uow_session, sort_by=sort_by, **kwargs
                )

            return None


class GetOneChannelHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_service = channel_service

    async def handle(self, **kwargs) -> ChannelResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_service.get_one_by_filters(
                    async_session=uow_session, filters=ChannelFilterModel(**kwargs)
                )

            return None


class CreateChannelHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_service = channel_service

    async def handle(
            self,
            create_model: ChannelCreateSchema,
    ) -> ChannelResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_service.create(
                    async_session=uow_session, create_model=create_model
                )

            return None


class UpdateContactHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_service = channel_service

    async def handle(
            self,
            update_model: ChannelUpdateSchema,
    ) -> ChannelResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_service.update(
                    async_session=uow_session, update_model=update_model
                )

            return None


class DeleteContactHandler(BaseDatabaseHandler):
    def __init__(
            self, channel_service: ChannelService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.channel_service = channel_service

    async def handle(
            self,
            uuid: UUID,
    ) -> int | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.channel_service.delete_one_by_uuid(
                    async_session=uow_session, uuid=uuid
                )

            return None
