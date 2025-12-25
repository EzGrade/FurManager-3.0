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
from src.core.orm.sorters.channel_config import ChannelConfigSortModel
from src.core.repositories.orm.base import BaseAbstractOrmRepository
from src.utils.types.transform_types import (
    ChannelConfigTransformOneCallback,
    ChannelConfigListTransformCallback,
    ChannelConfigTransformAllCallback,
)


class ChannelConfigRepository(BaseAbstractOrmRepository[ChannelConfigModelORM]):
    __model__ = ChannelConfigModelORM

    async def retrieve_one(
            self,
            filters: ChannelConfigFilterModel,
            transform: ChannelConfigTransformOneCallback,
            async_session: AsyncSession,
    ) -> ChannelConfigResponseSchema:
        entity = await super().get(filters=filters, async_session=async_session)
        return transform(entity)

    async def retrieve_list(
            self,
            filters: ChannelConfigFilterModel,
            async_session: AsyncSession,
            transform: ChannelConfigListTransformCallback,
            sorters: ChannelConfigSortModel,
            page: int | None = None,
            per_page: int | None = None,
    ) -> ManyResponseSchema[ChannelConfigResponseSchema]:
        entities = await super().get_list(
            filters=filters,
            sorters=sorters,
            page=page,  # type: ignore[arg-type]
            per_page=per_page,  # type: ignore[arg-type]
            async_session=async_session,
        )

        return transform(entities)

    async def retrieve_all(
            self,
            filters: ChannelConfigFilterModel,
            async_session: AsyncSession,
            transform: ChannelConfigTransformAllCallback,
            sorters: ChannelConfigSortModel | None = None,
    ) -> list[ChannelConfigResponseSchema]:
        entities = await super().get_all(
            filters=filters,
            async_session=async_session,
            sorters=sorters,
        )

        return transform(entities)

    async def create_one(
            self,
            model: ChannelConfigCreateSchema,
            transform: ChannelConfigTransformOneCallback,
            async_session: AsyncSession,
    ) -> ChannelConfigResponseSchema:
        created_key = await super().create(model, async_session)

        return await self.retrieve_one(
            filters=ChannelConfigFilterModel(uuid=created_key),
            transform=transform,
            async_session=async_session,
        )

    async def update_one(
            self,
            model: ChannelConfigUpdateSchema,
            transform: ChannelConfigTransformOneCallback,
            async_session: AsyncSession,
    ) -> ChannelConfigResponseSchema:
        updated_key = await super().update(
            ChannelConfigModelORM.uuid == model.uuid,
            model=model,
            async_session=async_session,
        )

        return await self.retrieve_one(
            filters=ChannelConfigFilterModel(uuid=updated_key),
            transform=transform,
            async_session=async_session,
        )

    async def delete_by_uuid(self, uuid: UUID, async_session: AsyncSession) -> int:
        return await super().delete(
            ChannelConfigModelORM.uuid == uuid, async_session=async_session
        )

    async def clear(self, async_session: AsyncSession) -> int:
        return await super().clear(async_session)
