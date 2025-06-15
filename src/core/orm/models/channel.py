from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.core.orm.models.base import BaseOrmModel


class ChannelModel(BaseOrmModel):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[str] = mapped_column(String, nullable=False)
