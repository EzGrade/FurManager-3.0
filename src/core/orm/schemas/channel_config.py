from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from src.core.orm.schemas.base import BaseModelSchema
from src.core.orm.schemas.user import UserResponseSchema


class ChannelConfigResponseSchema(BaseModelSchema):
    """
    Schema for channel response.
    """

    uuid: UUID = Field()
    is_post_owner_report_enabled: bool = Field(..., description="Is post owner report enabled?")

    updated_at: datetime = Field(..., description="Last update timestamp of the channel")
    updated_by_id: UUID | None = Field(None, description="UUID of the user who last updated the channel")
    channel_id: UUID | None = Field(None, description="UUID of the channel")

    def format(self, user: UserResponseSchema) -> str:
        post_owner_report_enabled = "Enabled" if self.is_post_owner_report_enabled else "Disabled"
        date = self.updated_at.strftime("%d %b %Y %H:%M:%S").replace("-", r"\-")
        return (
            f"Report post creator: {post_owner_report_enabled}\n"
            f"Last updated: {date}\\(UTC\\)\n"
            f"Updated by: @{user.username}\\({user.telegram_id}\\)"
        )


class ChannelConfigCreateSchema(BaseModelSchema):
    """
    Schema for creating a new channel.
    """

    uuid: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the channel"
    )
    is_post_owner_report_enabled: bool = Field(True, description="Is post owner report enabled?")

    updated_at: datetime | None = Field(None, description="Last update timestamp of the channel")
    updated_by_id: UUID | None = Field(None, description="UUID of the user who last updated the channel")
    channel_id: UUID | None = Field(None, description="UUID of the channel")


class ChannelConfigUpdateSchema(BaseModelSchema):
    """
    Schema for updating an existing channel.
    """

    uuid: UUID = Field(description="Unique identifier for the channel")
    is_post_owner_report_enabled: bool = Field(True, description="Is post owner report enabled?")

    updated_at: datetime | None = Field(None, description="Last update timestamp of the channel")
    updated_by_id: UUID | None = Field(None, description="UUID of the user who last updated the channel")
    channel_id: UUID | None = Field(None, description="UUID of the channel")
