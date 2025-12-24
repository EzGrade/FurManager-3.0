from uuid import UUID

from pydantic import Field

from src.core.models.base import BaseEntityModel


class ChannelModel(BaseEntityModel):
    uuid: UUID | None = Field(
        default=None,
        description="Unique identifier for the channel",
    )
    name: str | None = Field(
        default=None,
        description="Name of the channel",
    )
    title: str | None = Field(
        default=None,
        description="Title of the channel",
    )
    telegram_id: int = Field(
        ...,
        description="Unique Telegram identifier for the channel",
    )
    owner_id: UUID = Field(
        ...,
        description="UUID of the user who owns the channel",
    )
    created_at: str | None = Field(
        default=None,
        description="Creation timestamp of the channel",
    )
    updated_at: str | None = Field(
        default=None,
        description="Last update timestamp of the channel",
    )
