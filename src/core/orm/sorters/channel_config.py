from enum import StrEnum
from typing import Annotated

from pydantic import Field

from src.core.orm.sorters.base import BaseSortModel
from src.utils.enums.sort import SortOption


class ChannelConfigSortValues(StrEnum):
    uuid_asc = "uuid"
    uuid_desc = "-uuid"

    is_post_owner_report_enabled_asc = "is_post_owner_report_enabled"
    is_post_owner_report_enabled_desc = "-is_post_owner_report_enabled"

    updated_at_asc = "updated_at"
    updated_at_desc = "-updated_at"


class ChannelConfigSortModel(BaseSortModel):
    uuid: Annotated[SortOption | None, Field(default=None)]
    is_post_owner_report_enabled: Annotated[SortOption | None, Field(default=None)]
    updated_at: Annotated[SortOption | None, Field(default=None)]
