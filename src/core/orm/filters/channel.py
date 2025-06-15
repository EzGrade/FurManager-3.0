from typing import Annotated
from uuid import UUID

from sqlalchemy import text

from src.core.orm.filters.base import BaseFilterModel, Query
from src.core.orm.models import ChannelModelORM


class ChannelFilterModel(BaseFilterModel):
    uuid: Annotated[
        UUID | None, Query(filter_by=lambda i: ChannelModelORM.uuid == i)
    ] = None
    uuid__in: Annotated[
        list[UUID] | None, Query(filter_by=lambda i: ChannelModelORM.uuid.in_(i))
    ] = None

    name: Annotated[
        str | None,
        Query(filter_by=lambda n: text("name ILIKE :name").params(name=f"%{n}%")),
    ] = None
    name__in: Annotated[
        list[str] | None, Query(filter_by=lambda n: ChannelModelORM.name.in_(n))
    ] = None

    telegram_id: Annotated[
        int | None, Query(filter_by=lambda n: ChannelModelORM.telegram_id == n)
    ] = None
    telegram_id__in: Annotated[
        list[int] | None, Query(filter_by=lambda n: ChannelModelORM.telegram_id.in_(n))
    ] = None

    owner_id: Annotated[
        int | None, Query(filter_by=lambda n: ChannelModelORM.owner_id == n)
    ] = None
    owner_id__in: Annotated[
        list[int] | None, Query(filter_by=lambda n: ChannelModelORM.owner_id.in_(n))
    ] = None
