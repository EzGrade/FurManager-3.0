from typing import ClassVar, Annotated

from pydantic import BaseModel, ConfigDict, Field


class BaseEntityModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        extra="ignore",  # maybe set as forbid for better validation
    )


class ManyCustomResponse[T](BaseEntityModel):
    count: Annotated[int | None, Field()] = 0
    data: Annotated[list[T], Field()] = []
