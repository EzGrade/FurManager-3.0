from uuid import UUID as PYUUID, uuid4
from datetime import datetime, UTC

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.orm.models.base import BaseOrmModel


class ChannelModelORM(BaseOrmModel):
    __tablename__ = "channels"

    uuid: Mapped[PYUUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
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
