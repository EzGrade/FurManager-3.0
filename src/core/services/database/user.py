from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.orm.models import UserModelORM
from src.core.orm.filters.user import UserFilterModel
from src.core.orm.sorters.base import sort_convertor
from src.core.orm.sorters.user import UserSortValues, UserSortModel
from src.core.repositories.orm.user import UserRepository
from src.core.services.base import BaseService
from src.utils.transforms.orm.user import (
    transform_orm_user_model_into_response,
    transform_orm_user_model_into_many_responses,
    transform_orm_user_model_into_list_responses,
)
from src.core.orm.schemas.base import ManyResponseSchema
from src.core.orm.schemas.user import (
    UserResponseSchema,
    UserCreateSchema,
    UserUpdateSchema,
)


@dataclass
class UserServiceConfig:
    user_repository: UserRepository


class UserService(BaseService):
    def __init__(self, config: UserServiceConfig) -> None:
        self._repository = config.user_repository

    async def get_one_by_filters(
        self, filters: UserFilterModel, async_session: AsyncSession
    ) -> UserResponseSchema:
        return await self._repository.retrieve_one(
            filters=filters,
            transform=transform_orm_user_model_into_response,
            async_session=async_session,
        )

    async def get_list(
        self,
        async_session: AsyncSession,
        sort_by: UserSortValues,
        page: int | None = None,
        per_page: int | None = None,
        **kwargs,
    ) -> ManyResponseSchema[UserResponseSchema]:
        return await self._repository.retrieve_list(
            filters=UserFilterModel(**kwargs),
            sorters=sort_convertor(UserSortModel, sort_by),
            page=page,
            per_page=per_page,
            transform=transform_orm_user_model_into_many_responses,
            async_session=async_session,
        )

    async def get_all(
        self,
        async_session: AsyncSession,
        sort_by: UserSortValues | None = None,
        **kwargs,
    ) -> list[UserResponseSchema]:
        sorters = sort_convertor(UserSortModel, sort_by) if sort_by else None
        return await self._repository.retrieve_all(
            filters=UserFilterModel(**kwargs),
            sorters=sorters,
            async_session=async_session,
            transform=transform_orm_user_model_into_list_responses,
        )

    async def create(
        self, create_model: UserCreateSchema, async_session: AsyncSession
    ) -> UserResponseSchema:
        return await self._repository.create_one(
            model=create_model,
            transform=transform_orm_user_model_into_response,
            async_session=async_session,
        )

    async def create_all(
        self,
        create_models: list[UserCreateSchema],
        async_session: AsyncSession,
    ) -> int:
        return await self._repository.create_list(create_models, async_session)

    async def update(
        self, update_model: UserUpdateSchema, async_session: AsyncSession
    ) -> UserResponseSchema:
        return await self._repository.update_one(
            model=update_model,
            transform=transform_orm_user_model_into_response,
            async_session=async_session,
        )

    async def update_all(
        self, update_models: list[UserUpdateSchema], async_session: AsyncSession
    ) -> int:
        return await self._repository.update_list(update_models, async_session)

    async def delete_one_by_uuid(self, uuid: UUID, async_session: AsyncSession) -> int:
        return await self._repository.delete(
            UserModelORM.uuid == uuid, async_session=async_session
        )
