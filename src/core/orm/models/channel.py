from uuid import UUID as PYUUID

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.orm.models.base import BaseOrmModel


class ChannelModelORM(BaseOrmModel):
    __tablename__ = "channels"

    uuid: Mapped[PYUUID] = mapped_column(PGUUID, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[str] = mapped_column(String, nullable=False)
