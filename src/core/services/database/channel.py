from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.orm.models import ChannelModelORM
from src.core.orm.filters.channel import ChannelFilterModel
from src.core.orm.sorters.base import sort_convertor
from src.core.orm.sorters.channel import ChannelSortValues, ChannelSortModel
from src.core.repositories.orm.channel import ChannelRepository
from src.core.services.base import BaseService
from src.utils.transforms.orm.channel import (
    transform_orm_channel_model_into_response,
    transform_orm_channel_model_into_many_responses,
    transform_orm_channel_model_into_list_responses,
    transform_channel_model_into_create_request
)
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.channel import (
    ChannelResponseSchema,
    ChannelCreateSchema,
    ChannelUpdateSchema,
)


@dataclass
class ChannelServiceConfig:
    channel_repository: ChannelRepository


class ChannelService(BaseService):
    def __init__(self, config: ChannelServiceConfig) -> None:
        self._repository = config.channel_repository

    async def get_one_by_filters(
            self, filters: ChannelFilterModel, async_session: AsyncSession
    ) -> ChannelResponseSchema:
        return await self._repository.retrieve_one(
            filters=filters,
            transform=transform_orm_channel_model_into_response,
            async_session=async_session,
        )

    async def get_list(
            self,
            async_session: AsyncSession,
            sort_by: ChannelSortValues,
            page: int | None = None,
            per_page: int | None = None,
            **kwargs,
    ) -> ManyResponseSchema[ChannelResponseSchema]:
        return await self._repository.retrieve_list(
            filters=ChannelFilterModel(**kwargs),
            sorters=sort_convertor(ChannelSortModel, sort_by),
            page=page,
            per_page=per_page,
            transform=transform_orm_channel_model_into_many_responses,
            async_session=async_session,
        )

    async def get_all(
            self,
            async_session: AsyncSession,
            sort_by: ChannelSortValues | None = None,
            **kwargs,
    ) -> list[ChannelResponseSchema]:
        sorters = sort_convertor(ChannelSortModel, sort_by) if sort_by else None
        return await self._repository.retrieve_all(
            filters=ChannelFilterModel(**kwargs),
            sorters=sorters,
            async_session=async_session,
            transform=transform_orm_channel_model_into_list_responses,
        )

    async def create(
            self, create_model: ChannelCreateSchema, async_session: AsyncSession
    ) -> ChannelResponseSchema:
        return await self._repository.create_one(
            model=create_model,
            transform=transform_channel_model_into_create_request,
            async_session=async_session,
        )

    async def create_all(
            self,
            create_models: list[ChannelCreateSchema],
            async_session: AsyncSession,
    ) -> int:
        return await self._repository.create_list(create_models, async_session)

    async def update(
            self, update_model: ChannelUpdateSchema, async_session: AsyncSession
    ) -> ChannelResponseSchema:
        return await self._repository.update_one(
            model=update_model,
            transform=transform_orm_channel_model_into_response,
            async_session=async_session,
        )

    async def update_all(
            self, update_models: list[ChannelUpdateSchema], async_session: AsyncSession
    ) -> int:
        return await self._repository.update_list(update_models, async_session)

    async def delete_one_by_uuid(self, uuid: UUID, async_session: AsyncSession) -> int:
        return await self._repository.delete(
            ChannelModelORM.uuid == uuid, async_session=async_session
        )
