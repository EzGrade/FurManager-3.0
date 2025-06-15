from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.orm.filters.channel import ChannelFilterModel
from src.core.orm.models import ChannelModelORM
from src.core.orm.sorters.channel import ChannelSortModel
from src.core.repositories.orm.base import BaseAbstractOrmRepository
from src.utils.types.transform_types import (
    ChannelTransformOneCallback,
    ChannelListTransformCallback,
    ChannelTransformAllCallback,
)
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.channel import (
    ChannelResponseSchema,
    ChannelCreateSchema,
    ChannelUpdateSchema,
)


class ChannelRepository(BaseAbstractOrmRepository[ChannelModelORM]):
    __model__ = ChannelModelORM

    async def retrieve_one(
            self,
            filters: ChannelFilterModel,
            transform: ChannelTransformOneCallback,
            async_session: AsyncSession,
    ) -> ChannelResponseSchema:
        entity = await super().get(filters=filters, async_session=async_session)
        return transform(entity)

    async def retrieve_list(
            self,
            filters: ChannelFilterModel,
            async_session: AsyncSession,
            transform: ChannelListTransformCallback,
            sorters: ChannelSortModel,
            page: int | None = None,
            per_page: int | None = None,
    ) -> ManyResponseSchema[ChannelResponseSchema]:
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
            filters: ChannelFilterModel,
            async_session: AsyncSession,
            transform: ChannelTransformAllCallback,
            sorters: ChannelSortModel | None = None,
    ) -> list[ChannelResponseSchema]:
        entities = await super().get_all(
            filters=filters,
            async_session=async_session,
            sorters=sorters,
        )

        return transform(entities)

    async def create_one(
            self,
            model: ChannelCreateSchema,
            transform: ChannelTransformOneCallback,
            async_session: AsyncSession,
    ) -> ChannelResponseSchema:
        created_key = await super().create(model, async_session)

        return await self.retrieve_one(
            filters=ChannelFilterModel(uuid=created_key),
            transform=transform,
            async_session=async_session,
        )

    async def update_one(
            self,
            model: ChannelUpdateSchema,
            transform: ChannelTransformOneCallback,
            async_session: AsyncSession,
    ) -> ChannelResponseSchema:
        updated_key = await super().update(
            ChannelModelORM.uuid == model.uuid,
            model=model,
            async_session=async_session,
        )

        return await self.retrieve_one(
            filters=ChannelFilterModel(uuid=updated_key),
            transform=transform,
            async_session=async_session,
        )

    async def delete_by_uuid(self, uuid: UUID, async_session: AsyncSession) -> int:
        return await super().delete(
            ChannelModelORM.uuid == uuid, async_session=async_session
        )

    async def delete_by_telegram_id(
            self, telegram_id: int, async_session: AsyncSession
    ) -> int:
        return await super().delete(
            ChannelModelORM.telegram_id == telegram_id, async_session=async_session
        )

    async def clear(self, async_session: AsyncSession) -> int:
        return await super().clear(async_session)
