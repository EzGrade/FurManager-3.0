from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.orm.filters.user import UserFilterModel
from src.core.orm.models import UserModelORM
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.user import (
    UserResponseSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from src.core.orm.sorters.user import UserSortModel
from src.core.repositories.orm.base import BaseAbstractOrmRepository
from src.utils.types.transform_types import (
    UserTransformOneCallback,
    UserListTransformCallback,
    UserTransformAllCallback,
)


class UserRepository(BaseAbstractOrmRepository[UserModelORM]):
    __model__ = UserModelORM

    async def retrieve_one(
            self,
            filters: UserFilterModel,
            transform: UserTransformOneCallback,
            async_session: AsyncSession,
    ) -> UserResponseSchema:
        entity = await super().get(filters=filters, async_session=async_session)
        return transform(entity)

    async def retrieve_list(
            self,
            filters: UserFilterModel,
            async_session: AsyncSession,
            transform: UserListTransformCallback,
            sorters: UserSortModel,
            page: int | None = None,
            per_page: int | None = None,
    ) -> ManyResponseSchema[UserResponseSchema]:
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
            filters: UserFilterModel,
            async_session: AsyncSession,
            transform: UserTransformAllCallback,
            sorters: UserSortModel | None = None,
    ) -> list[UserResponseSchema]:
        entities = await super().get_all(
            filters=filters,
            async_session=async_session,
            sorters=sorters,
        )

        return transform(entities)

    async def create_one(
            self,
            model: UserCreateSchema,
            transform: UserTransformOneCallback,
            async_session: AsyncSession,
    ) -> UserResponseSchema:
        created_key = await super().create(model, async_session)

        return await self.retrieve_one(
            filters=UserFilterModel(uuid=created_key),
            transform=transform,
            async_session=async_session,
        )

    async def update_one(
            self,
            model: UserUpdateSchema,
            transform: UserTransformOneCallback,
            async_session: AsyncSession,
    ) -> UserResponseSchema:
        updated_key = await super().update(
            UserModelORM.uuid == model.uuid,
            model=model,
            async_session=async_session,
        )

        return await self.retrieve_one(
            filters=UserFilterModel(uuid=updated_key),
            transform=transform,
            async_session=async_session,
        )

    async def delete_by_uuid(self, uuid: UUID, async_session: AsyncSession) -> int:
        return await super().delete(
            UserModelORM.uuid == uuid, async_session=async_session
        )

    async def delete_by_telegram_id(
            self, telegram_id: int, async_session: AsyncSession
    ) -> int:
        return await super().delete(
            UserModelORM.telegram_id == telegram_id, async_session=async_session
        )

    async def clear(self, async_session: AsyncSession) -> int:
        return await super().clear(async_session)
