from datetime import datetime, UTC
from typing import TYPE_CHECKING
from uuid import UUID as PYUUID, uuid4

from sqlalchemy import String, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.orm.models.base import BaseOrmModel

if TYPE_CHECKING:
    from src.core.orm.models.user import UserModelORM
    from src.core.orm.models.channel_config import ChannelConfigModelORM


class ChannelModelORM(BaseOrmModel):
    __tablename__ = "channels"

    uuid: Mapped[PYUUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    owner_id: Mapped[PYUUID] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        insert_default=lambda: datetime.now(UTC).replace(tzinfo=None),
        nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        insert_default=lambda: datetime.now(UTC).replace(tzinfo=None),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    owner: Mapped["UserModelORM"] = relationship(back_populates="channels")
    config: Mapped["ChannelConfigModelORM"] = relationship(
        back_populates="channel", uselist=False, cascade="all, delete-orphan"
    )
