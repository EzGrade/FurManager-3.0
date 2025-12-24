from datetime import datetime, UTC
from typing import TYPE_CHECKING
from uuid import UUID as PYUUID, uuid4

from sqlalchemy import String, BigInteger, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.orm.models.base import BaseOrmModel

if TYPE_CHECKING:
    from src.core.orm.models.user import UserModelORM


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
        nullable=False
    )
    owner: Mapped["UserModelORM"] = relationship(back_populates="channels")
