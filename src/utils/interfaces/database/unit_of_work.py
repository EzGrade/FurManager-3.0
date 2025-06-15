from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UnitOfWork:
    def __init__(self, async_session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = async_session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self.session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if self.session is not None:
            if exc_type:
                # Add log for exception
                await self.rollback()
            else:
                await self.commit()

            await self.session.close()

    async def commit(self) -> None:
        if self.session is not None:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session is not None:
            await self.session.rollback()
