from uuid import UUID

from src.core.orm.filters.user import UserFilterModel
from src.core.orm.schemas.user import (
    UserResponseSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from src.core.orm.sorters.user import UserSortValues
from src.core.services.database.user import UserService
from src.utils.exceptions.database.orm import NoRecordsFoundException
from src.utils.interfaces.database.unit_of_work import UnitOfWork
from src.utils.interfaces.handler import BaseDatabaseHandler


class GetAllUsersHandler(BaseDatabaseHandler):
    def __init__(
            self, user_service: ..., unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.user_service = user_service

    async def handle(
            self, sort_by: UserSortValues | None = None, **kwargs
    ) -> list[UserResponseSchema] | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.user_service.get_all(
                    async_session=uow_session, sort_by=sort_by, **kwargs
                )

            return None


class GetOneUserHandler(BaseDatabaseHandler):
    def __init__(
            self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.user_service = user_service

    async def handle(self, **kwargs) -> UserResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                try:
                    return await self.user_service.get_one_by_filters(
                        async_session=uow_session, filters=UserFilterModel(**kwargs)
                    )
                except NoRecordsFoundException:
                    return None

            return None


class CreateUserHandler(BaseDatabaseHandler):
    def __init__(
            self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.user_service = user_service

    async def handle(
            self,
            create_model: UserCreateSchema,
    ) -> UserResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.user_service.create(
                    async_session=uow_session, create_model=create_model
                )

            return None


class UpdateUserHandler(BaseDatabaseHandler):
    def __init__(
            self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.user_service = user_service

    async def handle(
            self,
            update_model: UserUpdateSchema,
    ) -> UserResponseSchema | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.user_service.update(
                    async_session=uow_session, update_model=update_model
                )

            return None


class DeleteUserHandler(BaseDatabaseHandler):
    def __init__(
            self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> None:
        super().__init__(unit_of_work)
        self.user_service = user_service

    async def handle(
            self,
            uuid: UUID,
    ) -> int | None:
        async with self.unit_of_work as unit_of_work:
            uow_session = unit_of_work.session
            if uow_session is not None:
                return await self.user_service.delete_one_by_uuid(
                    async_session=uow_session, uuid=uuid
                )

            return None
