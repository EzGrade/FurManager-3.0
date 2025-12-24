from typing import Annotated
from uuid import UUID
from datetime import datetime

from sqlalchemy import text

from src.core.orm.filters.base import BaseFilterModel, Query
from src.core.orm.models import UserModelORM


class UserFilterModel(BaseFilterModel):
    uuid: Annotated[
        UUID | None, Query(filter_by=lambda i: UserModelORM.uuid == i)
    ] = None
    uuid__in: Annotated[
        list[UUID] | None, Query(filter_by=lambda i: UserModelORM.uuid.in_(i))
    ] = None

    first_name: Annotated[
        str | None,
        Query(filter_by=lambda n: text("name ILIKE :first_name").params(first_name=f"%{n}%")),
    ] = None
    first_name__in: Annotated[
        list[str] | None, Query(filter_by=lambda n: UserModelORM.first_name.in_(n))
    ] = None

    last_name: Annotated[
        str | None,
        Query(filter_by=lambda n: text("name ILIKE :last_name").params(last_name=f"%{n}%")),
    ] = None
    last_name__in: Annotated[
        list[str] | None, Query(filter_by=lambda n: UserModelORM.last_name.in_(n))
    ] = None

    username: Annotated[
        str | None,
        Query(filter_by=lambda n: text("title ILIKE :username").params(username=f"%{n}%")),
    ] = None
    username__in: Annotated[
        list[str] | None, Query(filter_by=lambda n: UserModelORM.username.in_(n))
    ] = None

    telegram_id: Annotated[
        int | None, Query(filter_by=lambda n: UserModelORM.telegram_id == n)
    ] = None
    telegram_id__in: Annotated[
        list[int] | None, Query(filter_by=lambda n: UserModelORM.telegram_id.in_(n))
    ] = None

    joined_at: Annotated[
        datetime | None, Query(filter_by=lambda n: UserModelORM.joined_at == n)
    ] = None
