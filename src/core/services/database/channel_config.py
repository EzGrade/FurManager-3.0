from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.orm.filters.channel_config import ChannelConfigFilterModel
from src.core.orm.models import ChannelConfigModelORM
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.channel_config import (
    ChannelConfigResponseSchema,
    ChannelConfigCreateSchema,
    ChannelConfigUpdateSchema,
)
from src.core.orm.sorters.base import sort_convertor
from src.core.orm.sorters.channel_config import ChannelConfigSortValues, ChannelConfigSortModel
from src.core.repositories.orm.channel_config import ChannelConfigRepository
from src.core.services.base import BaseService
from src.utils.transforms.orm.channel_config import (
    transform_orm_channel_config_model_into_response,
    transform_orm_channel_config_model_into_many_responses,
    transform_orm_channel_config_model_into_list_responses,
)


@dataclass
class ChannelConfigServiceConfig:
    channel_config_repository: ChannelConfigRepository


class ChannelConfigService(BaseService):
    def __init__(self, config: ChannelConfigServiceConfig) -> None:
        self._repository = config.channel_config_repository

    async def get_one_by_filters(
            self, filters: ChannelConfigFilterModel, async_session: AsyncSession
    ) -> ChannelConfigResponseSchema:
        return await self._repository.retrieve_one(
            filters=filters,
            transform=transform_orm_channel_config_model_into_response,
            async_session=async_session,
        )

    async def get_list(
            self,
            async_session: AsyncSession,
            sort_by: ChannelConfigSortValues,
            page: int | None = None,
            per_page: int | None = None,
            **kwargs,
    ) -> ManyResponseSchema[ChannelConfigResponseSchema]:
        return await self._repository.retrieve_list(
            filters=ChannelConfigFilterModel(**kwargs),
            sorters=sort_convertor(ChannelConfigSortModel, sort_by),
            page=page,
            per_page=per_page,
            transform=transform_orm_channel_config_model_into_many_responses,
            async_session=async_session,
        )

    async def get_all(
            self,
            async_session: AsyncSession,
            sort_by: ChannelConfigSortValues | None = None,
            **kwargs,
    ) -> list[ChannelConfigResponseSchema]:
        sorters = sort_convertor(ChannelConfigSortModel, sort_by) if sort_by else None
        return await self._repository.retrieve_all(
            filters=ChannelConfigFilterModel(**kwargs),
            sorters=sorters,
            async_session=async_session,
            transform=transform_orm_channel_config_model_into_list_responses,
        )

    async def create(
            self, create_model: ChannelConfigCreateSchema, async_session: AsyncSession
    ) -> ChannelConfigResponseSchema:
        return await self._repository.create_one(
            model=create_model,
            transform=transform_orm_channel_config_model_into_response,
            async_session=async_session,
        )

    async def create_all(
            self,
            create_models: list[ChannelConfigCreateSchema],
            async_session: AsyncSession,
    ) -> int:
        return await self._repository.create_list(create_models, async_session)

    async def update(
            self, update_model: ChannelConfigUpdateSchema, async_session: AsyncSession
    ) -> ChannelConfigResponseSchema:
        return await self._repository.update_one(
            model=update_model,
            transform=transform_orm_channel_config_model_into_response,
            async_session=async_session,
        )

    async def update_all(
            self, update_models: list[ChannelConfigUpdateSchema], async_session: AsyncSession
    ) -> int:
        return await self._repository.update_list(update_models, async_session)

    async def delete_one_by_uuid(self, uuid: UUID, async_session: AsyncSession) -> int:
        return await self._repository.delete(
            ChannelConfigModelORM.uuid == uuid, async_session=async_session
        )
