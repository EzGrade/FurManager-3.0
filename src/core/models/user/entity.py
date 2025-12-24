from uuid import UUID

from pydantic import Field

from src.core.models.base import BaseEntityModel


class UserModel(BaseEntityModel):
    uuid: UUID | None = Field(
        default=None,
        description="Unique identifier for the user",
    )
    first_name: str | None = Field(
        default=None,
        description="First Name of the user",
    )
    last_name: str | None = Field(
        default=None,
        description="Last Name of the user",
    )
    username: str | None = Field(
        default=None,
        description="Username of the user",
    )
    telegram_id: int = Field(
        ...,
        description="Unique Telegram identifier for the user",
    )
    joined_at: str | None = Field(
        default=None,
        description="Joining timestamp of the user",
    )
