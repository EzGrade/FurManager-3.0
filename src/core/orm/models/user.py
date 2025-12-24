from datetime import datetime, UTC
from typing import TYPE_CHECKING
from uuid import UUID as PYUUID, uuid4

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.orm.models.base import BaseOrmModel

if TYPE_CHECKING:
    from src.core.orm.models.channel import ChannelModelORM


class UserModelORM(BaseOrmModel):
    __tablename__ = "users"

    uuid: Mapped[PYUUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    joined_at: Mapped[DateTime] = mapped_column(
        DateTime,
        insert_default=lambda: datetime.now(UTC).replace(tzinfo=None),
        nullable=False
    )

    channels: Mapped[list["ChannelModelORM"]] = relationship(back_populates="owner")
