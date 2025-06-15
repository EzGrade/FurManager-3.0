from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import ColumnExpressionArgument, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import ManyCustomResponse
from src.orm.models import BaseOrmModel
from src.utils.types.type_variables import (
    FilterModelT,
    SortModelT,
    CreateModelT,
    UpdateModelT,
)


class OrmRepositoryInterface[AbstractModel: BaseOrmModel](ABC):
    """Base ORM repository interface with CRUD operations"""

    @abstractmethod
    async def get(
        self, filters: FilterModelT, async_session: AsyncSession
    ) -> AbstractModel:
        raise NotImplementedError("Method 'get' is not implemented")

    @abstractmethod
    async def get_list(
        self,
        filters: FilterModelT,
        sorters: SortModelT,
        async_session: AsyncSession,
        page: int = 0,
        per_page: int = 5,
    ) -> ManyCustomResponse:
        raise NotImplementedError("Method 'get_list' is not implemented")

    @abstractmethod
    async def get_all(
        self,
        filters: FilterModelT,
        async_session: AsyncSession,
        sorters: SortModelT | None = None,
    ) -> Sequence[AbstractModel]:
        raise NotImplementedError("Method 'get_all' is not implemented")

    @abstractmethod
    async def create(
        self, model: CreateModelT, async_session: AsyncSession
    ) -> AbstractModel:
        raise NotImplementedError("Method 'create' is not implemented")

    @abstractmethod
    async def create_list(self, models: list[CreateModelT], async_session) -> int:
        raise NotImplementedError("Method 'create_list' is not implemented")

    @abstractmethod
    async def update(
        self,
        *clauses: ColumnExpressionArgument,
        model: UpdateModelT,
        async_session: AsyncSession,
    ):
        raise NotImplementedError("Method 'update' is not implemented")

    @abstractmethod
    async def update_list(
        self, models: list[UpdateModelT], async_session: AsyncSession
    ) -> ScalarResult:
        raise NotImplementedError("Method 'update_list' is not implemented")

    @abstractmethod
    async def delete(
        self, *clauses: ColumnExpressionArgument, async_session: AsyncSession
    ) -> int:
        raise NotImplementedError("Method 'delete' is not implemented")
