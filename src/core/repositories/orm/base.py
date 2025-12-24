from typing import Sequence, Type

import loguru
from sqlalchemy import (
    select,
    delete,
    insert,
    update,
    func,
    ColumnExpressionArgument,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.base import ManyCustomResponse
from src.core.orm.models.base import BaseOrmModel
from src.utils.exceptions.database.orm import NoRecordsFoundException
from src.utils.interfaces.database.repository import OrmRepositoryInterface
from src.utils.types.type_variables import (
    CreateModelT,
    FilterModelT,
    SortModelT,
    UpdateModelT,
)


class BaseAbstractOrmRepository[AbstractModel: BaseOrmModel](OrmRepositoryInterface):
    """
    Generic base repository with CRUD operations.
    """

    __model__: Type[AbstractModel]

    async def get(
        self,
        filters: FilterModelT,
        async_session: AsyncSession,
    ) -> AbstractModel:
        sql = filters.generate_filtered_query(expression=select(self.__model__))
        result = await async_session.execute(sql)
        if not (orm_model := result.scalar_one_or_none()):
            message = f"Unable to get: does not have any records for sql: {sql} by provided filters: {filters}"
            loguru.logger.warning(message)
            raise NoRecordsFoundException(
                message=message,
                details={"Object": f"<{self.__model__}>"},
            )

        return orm_model

    async def get_list(
        self,
        filters: FilterModelT,
        sorters: SortModelT,
        async_session: AsyncSession,
        page: int = 1,
        per_page: int = 5,
    ) -> ManyCustomResponse:
        filtered_query = filters.generate_filtered_query(
            expression=select(self.__model__)
        )

        result = await async_session.execute(
            filtered_query.order_by(*sorters.generate_params())
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        data = list(result.scalars().all())

        count_result = await async_session.execute(
            select(func.count()).select_from(filtered_query.subquery())
        )
        count = count_result.scalar()

        return ManyCustomResponse[self.__model__](count=count, data=data)  # type: ignore[name-defined]

    async def get_all(
        self,
        filters: FilterModelT,
        async_session: AsyncSession,
        sorters: SortModelT | None = None,
    ) -> Sequence[AbstractModel]:
        filtered_query = filters.generate_filtered_query(
            expression=select(self.__model__)
        )

        if sorters:
            filtered_query = filtered_query.order_by(*sorters.generate_params())

        results = await async_session.execute(filtered_query)
        return results.scalars().all()

    async def create(self, model: CreateModelT, async_session: AsyncSession):
        stmt = (
            insert(self.__model__)
            .values(model.model_dump(exclude_unset=True, exclude_none=True))
            .returning(*self.__model__.__table__.columns)
        )
        return (await async_session.execute(statement=stmt)).scalar()

    async def create_list(
        self, models: list[CreateModelT], async_session: AsyncSession
    ) -> int:
        stmt = insert(self.__model__).values(
            [model.model_dump(exclude_unset=True, exclude_none=True) for model in models]
        )

        return (await async_session.execute(statement=stmt)).rowcount

    async def update(
        self,
        *clauses: ColumnExpressionArgument,
        model: UpdateModelT,
        async_session: AsyncSession,
    ):
        stmt = (
            update(self.__model__)
            .where(*clauses)
            .values(model.model_dump(exclude_unset=True, exclude_none=True))
            .returning(*self.__model__.__table__.columns)
        )

        return (await async_session.execute(statement=stmt)).scalar()

    async def update_list(
        self, models: list[UpdateModelT], async_session: AsyncSession
    ):
        """TODO Experiment with result"""
        result = await async_session.execute(
            update(self.__model__),
            [model.model_dump(exclude_unset=True, exclude_none=True) for model in models],
        )
        return result.scalar()

    async def delete(
        self, *clauses: ColumnExpressionArgument, async_session: AsyncSession
    ) -> int:
        stmt = delete(self.__model__).where(*clauses)

        return (await async_session.execute(statement=stmt)).rowcount

    async def clear(self, async_session: AsyncSession):
        await async_session.execute(delete(self.__model__))
        return None
