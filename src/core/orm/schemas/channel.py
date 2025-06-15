from uuid import UUID, uuid4

from pydantic import Field

from src.core.orm.schemas.base import BaseModelSchema


class ChannelResponseSchema(BaseModelSchema):
    """
    Schema for channel response.
    """

    uuid: UUID = Field()
    name: str = Field(..., description="Name of the channel")
    telegram_id: int = Field(..., description="Telegram ID of the channel")
    owner_id: int = Field(..., description="Owner ID of the channel")


class ChannelCreateSchema(BaseModelSchema):
    """
    Schema for creating a new channel.
    """

    uuid: UUID | None = Field(default_factory=uuid4, description="Unique identifier for the channel")
    name: str = Field(..., description="Name of the channel")
    telegram_id: int = Field(..., description="Telegram ID of the channel")
    owner_id: int = Field(..., description="Owner ID of the channel")


class ChannelUpdateSchema(BaseModelSchema):
    """
    Schema for updating an existing channel.
    """

    name: str | None = Field(None, description="Name of the channel")
    telegram_id: int | None = Field(None, description="Telegram ID of the channel")
    owner_id: int = Field(..., description="Owner ID of the channel")
