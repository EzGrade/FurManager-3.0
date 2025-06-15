from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.core.models.base import ManyCustomResponse


class BaseModelSchema(BaseModel):
    """Base model for all request and response schemas"""

    model_config = ConfigDict(
        extra="ignore",
        from_attributes=True,
    )


class BaseDatabaseModelSchema(BaseModelSchema):
    id: Annotated[int, Field()]


class BaseResponseSchema[T](BaseModelSchema, populate_by_name=True):
    payload: Annotated[T | list[T], Field()]


class ManyResponseSchema[T](ManyCustomResponse[T], populate_by_name=True):
    count: Annotated[int | None, Field(alias="totalItems")] = 0
    data: Annotated[list[T], Field(default_factory=list, alias="currentPageItems")]


class ManyRequestSchema(BaseModelSchema):
    per_page: Annotated[int, Field(ge=1, default=5, alias="pageSize")]
    page: Annotated[int, Field(ge=1, default=1, alias="pageIndex")]
