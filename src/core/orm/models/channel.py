from uuid import UUID as PYUUID, uuid4

from sqlalchemy import String, BigInteger
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.orm.models.base import BaseOrmModel


class ChannelModelORM(BaseOrmModel):
    __tablename__ = "channels"

    uuid: Mapped[PYUUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, nullable=False)