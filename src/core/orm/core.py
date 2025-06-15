from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)


class Database:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.async_engine = create_async_engine(
            db_url, pool_pre_ping=True, pool_size=30, max_overflow=0
        )

        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def session(self):
        session = self.async_session_maker()
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(f"Error in session\n{e}")
            await session.rollback()
            raise
        finally:
            await session.close()
