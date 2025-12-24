from dishka import Provider, Scope, provide

from src.config.database import PostgresConfig
from src.utils.interfaces.database.unit_of_work import UnitOfWork
from src.core.services.database.user import UserServiceConfig, UserService
from src.core.repositories.orm.user import UserRepository
from src.core.orm.handlers.user import (
    GetAllUsersHandler,
    GetOneUserHandler,
    CreateUserHandler,
    UpdateUserHandler,
    DeleteUserHandler,
)
from src.core.orm.core import Database


class UserProvider(Provider):
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
    def provide_user_repository(self) -> UserRepository:
        """Provides an instance of the UserRepository."""
        return UserRepository()

    @provide(scope=Scope.REQUEST)
    def provide_user_service(
        self, user_repository: UserRepository
    ) -> UserService:
        """Provides an instance of the UserService."""
        config = UserServiceConfig(user_repository=user_repository)
        return UserService(config=config)

    @provide(scope=Scope.REQUEST)
    def provide_get_all_users_handler(
        self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> GetAllUsersHandler:
        """Provides an instance of the GetAllUsersHandler."""
        return GetAllUsersHandler(
            user_service=user_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_get_one_user_handler(
        self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> GetOneUserHandler:
        """Provides an instance of the GetOneUserHandler."""
        return GetOneUserHandler(
            user_service=user_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_create_user_handler(
        self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> CreateUserHandler:
        """Provides an instance of the CreateUserHandler."""
        return CreateUserHandler(
            user_service=user_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_update_user_handler(
        self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> UpdateUserHandler:
        """Provides an instance of the UpdateUserHandler."""
        return UpdateUserHandler(
            user_service=user_service, unit_of_work=unit_of_work
        )

    @provide(scope=Scope.REQUEST)
    def provide_delete_user_handler(
        self, user_service: UserService, unit_of_work: UnitOfWork
    ) -> DeleteUserHandler:
        """Provides an instance of the DeleteUserHandler."""
        return DeleteUserHandler(
            user_service=user_service, unit_of_work=unit_of_work
        )
