from datetime import datetime, UTC
from typing import TYPE_CHECKING
from uuid import UUID as PYUUID, uuid4

from sqlalchemy import DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.orm.models.base import BaseOrmModel

if TYPE_CHECKING:
    from src.core.orm.models.channel import ChannelModelORM
    from src.core.orm.models.user import UserModelORM


class ChannelConfigModelORM(BaseOrmModel):
    __tablename__ = "channel_configs"

    uuid: Mapped[PYUUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)
    is_post_owner_report_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    channel_id: Mapped[PYUUID] = mapped_column(ForeignKey("channels.uuid"), nullable=True, unique=True)
    updated_by_id: Mapped[PYUUID | None] = mapped_column(ForeignKey("users.uuid"), nullable=True)

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        insert_default=lambda: datetime.now(UTC).replace(tzinfo=None),
        nullable=False
    )

    channel: Mapped["ChannelModelORM"] = relationship(back_populates="config", uselist=False)
    updated_by: Mapped["UserModelORM"] = relationship(back_populates="channels_configs")
