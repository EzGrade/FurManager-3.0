from enum import StrEnum
from typing import Annotated

from pydantic import Field

from src.core.orm.sorters.base import BaseSortModel
from src.utils.enums.sort import SortOption


class UserSortValues(StrEnum):
    uuid_asc = "uuid"
    uuid_desc = "-uuid"

    first_name_asc = "first_name"
    first_name_desc = "-first_name"
    
    last_name_asc = "last_name"
    last_name_desc = "-last_name"

    username_asc = "username"
    username_desc = "-username"

    telegram_id_asc = "telegram_id"
    telegram_id_desc = "-telegram_id"

    joined_at_asc = "joined_at"
    joined_at_desc = "-joined_at"

class UserSortModel(BaseSortModel):
    uuid: Annotated[SortOption | None, Field(default=None)]
    first_name: Annotated[SortOption | None, Field(default=None)]
    last_name: Annotated[SortOption | None, Field(default=None)]
    username: Annotated[SortOption | None, Field(default=None)]
    telegram_id: Annotated[SortOption | None, Field(default=None)]
    joined_at: Annotated[SortOption | None, Field(default=None)]
