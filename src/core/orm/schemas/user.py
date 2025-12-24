from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from src.core.orm.schemas.base import BaseModelSchema


class UserResponseSchema(BaseModelSchema):
    """
    Schema for user response.
    """

    uuid: UUID = Field()
    first_name: str | None = Field(None, description="First Name of the user")
    last_name: str | None = Field(None, description="Last Name of the user")
    username: str | None = Field(None, description="Username of the user")
    telegram_id: int = Field(..., description="Telegram ID of the user")

    joined_at: datetime = Field(..., description="Joining timestamp of the user")


class UserCreateSchema(BaseModelSchema):
    """
    Schema for creating a new user.
    """

    uuid: UUID | None = Field(
        default_factory=uuid4, description="Unique identifier for the channel"
    )
    first_name: str | None = Field(None, description="First Name of the user")
    last_name: str | None = Field(None, description="Last Name of the user")
    username: str | None = Field(None, description="Username of the user")
    telegram_id: int = Field(..., description="Telegram ID of the user")

    joined_at: datetime | None = Field(None, description="Joining timestamp of the user")


class UserUpdateSchema(BaseModelSchema):
    """
    Schema for updating an existing user.
    """

    uuid: UUID = Field(description="Unique identifier for the user")
    first_name: str | None = Field(None, description="First Name of the user")
    last_name: str | None = Field(None, description="Last Name of the user")
    telegram_id: int = Field(..., description="Telegram ID of the user")
