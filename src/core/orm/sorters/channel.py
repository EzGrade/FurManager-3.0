from enum import StrEnum
from typing import Annotated

from pydantic import Field

from src.core.orm.sorters.base import BaseSortModel
from src.utils.enums.sort import SortOption


class ChannelSortValues(StrEnum):
    uuid_asc = "uuid"
    uuid_desc = "-uuid"

    name_asc = "name"
    name_desc = "-name"

    title_asc = "title"
    title_desc = "-title"

    telegram_id_asc = "telegram_id"
    telegram_id_desc = "-telegram_id"


class ChannelSortModel(BaseSortModel):
    uuid: Annotated[SortOption | None, Field(default=None)]
    name: Annotated[SortOption | None, Field(default=None)]
    title: Annotated[SortOption | None, Field(default=None)]
    telegram_id: Annotated[SortOption | None, Field(default=None)]
