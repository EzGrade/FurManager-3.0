from uuid import UUID, uuid4

from pydantic import Field

from src.core.models.base import BaseEntityModel


class ChannelModel(BaseEntityModel):
    uuid: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for the channel",
    )
    telegram_id: int = Field(
        ...,
        description="Unique Telegram identifier for the channel",
    )
    name: str | None = Field(
        default=None,
        description="Name of the channel",
    )
    owner_id: int = Field(
        ...,
        description="ID of the user who owns the channel",
    )
