from uuid import UUID

from pydantic import Field

from src.core.models.base import BaseEntityModel


class ChannelConfigModel(BaseEntityModel):
    uuid: UUID | None = Field(
        default=None,
        description="Unique identifier for the channel",
    )
    is_post_owner_report_enabled: bool = Field(True, description="Is post owner report enabled?")

    updated_at: str | None = Field(
        default=None,
        description="Last update timestamp of the channel",
    )
    updated_by: UUID = Field(..., description="UUID of the user who last updated the channel")
    channel: UUID = Field(..., description="UUID of the channel")
