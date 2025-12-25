from datetime import datetime
from typing import Annotated
from uuid import UUID

from src.core.orm.filters.base import BaseFilterModel, Query
from src.core.orm.models import ChannelConfigModelORM


class ChannelConfigFilterModel(BaseFilterModel):
    uuid: Annotated[
        UUID | None, Query(filter_by=lambda i: ChannelConfigModelORM.uuid == i)
    ] = None
    uuid__in: Annotated[
        list[UUID] | None, Query(filter_by=lambda i: ChannelConfigModelORM.uuid.in_(i))
    ] = None

    is_post_owner_report_enabled: Annotated[
        bool | None, Query(filter_by=lambda i: ChannelConfigModelORM.is_post_owner_report_enabled == i)
    ] = None

    updated_at: Annotated[
        datetime | None, Query(filter_by=lambda n: ChannelConfigModelORM.updated_at == n)
    ] = None

    updated_by_id: Annotated[
        UUID | None, Query(filter_by=lambda n: ChannelConfigModelORM.updated_by_id == n)
    ] = None
    updated_by_id__in: Annotated[
        list[UUID] | None, Query(filter_by=lambda n: ChannelConfigModelORM.updated_by_id.in_(n))
    ] = None

    channel_id: Annotated[
        UUID | None, Query(filter_by=lambda n: ChannelConfigModelORM.channel_id == n)
    ] = None
