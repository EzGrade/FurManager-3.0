from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import Field

from src.core.orm.schemas.base import BaseModelSchema


class ChannelResponseSchema(BaseModelSchema):
    """
    Schema for channel response.
    """

    uuid: UUID = Field()
    name: str | None = Field(None, description="Name of the channel")
    title: str | None = Field(None, description="Title of the channel")
    telegram_id: int = Field(..., description="Telegram ID of the channel")
    owner_id: UUID = Field(..., description="Owner UUID of the channel")

    created_at: datetime = Field(..., description="Creation timestamp of the channel")
    updated_at: datetime = Field(..., description="Last update timestamp of the channel")

    def format(self) -> str:
        title = self.title if self.title is not None else "No title"
        name = f"@{self.name}" if self.name is not None else "No name"
        telegram_id = f"`{self.telegram_id}`"

        return f"Title: {title}\n  \\- Name: {name}\n  \\- Telegram ID: {telegram_id}"


class ChannelCreateSchema(BaseModelSchema):
    """
    Schema for creating a new channel.
    """

    uuid: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the channel"
    )
    name: str | None = Field(None, description="Name of the channel")
    title: str | None = Field(None, description="Title of the channel")
    telegram_id: int = Field(..., description="Telegram ID of the channel")
    owner_id: UUID = Field(..., description="Owner UUID of the channel")

    created_at: datetime | None = Field(
        description="Creation timestamp of the channel",
        default=None
    )
    updated_at: datetime | None = Field(
        description="Last update timestamp of the channel",
        default=None
    )


class ChannelUpdateSchema(BaseModelSchema):
    """
    Schema for updating an existing channel.
    """

    uuid: UUID = Field(description="Unique identifier for the channel")
    name: str | None = Field(None, description="Name of the channel")
    title: str | None = Field(None, description="Title of the channel")
    telegram_id: int | None = Field(None, description="Telegram ID of the channel")
    owner_id: UUID = Field(..., description="Owner UUID of the channel")

    updated_at: datetime | None = Field(
        description="Last update timestamp of the channel",
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None),
    )
