from uuid import UUID

from pydantic import Field

from src.core.orm.schemas.base import BaseModelSchema


class ChannelResponseSchema(BaseModelSchema):
    """
    Schema for channel response.
    """

    uuid: UUID = Field()
    name: str = Field(..., description="Name of the channel")
    telegram_id: str = Field(..., description="Telegram ID of the channel")


class ChannelCreateSchema(BaseModelSchema):
    """
    Schema for creating a new channel.
    """

    name: str = Field(..., description="Name of the channel")
    telegram_id: str = Field(..., description="Telegram ID of the channel")


class ChannelUpdateSchema(BaseModelSchema):
    """
    Schema for updating an existing channel.
    """

    name: str | None = Field(None, description="Name of the channel")
    telegram_id: str | None = Field(None, description="Telegram ID of the channel")
