from abc import ABC, abstractmethod

from src.utils.interfaces.database.unit_of_work import UnitOfWork


class BaseHandler(ABC): ...


class Handler(BaseHandler):
    """Handler for a logic-component which work with integration e.t.c"""

    @abstractmethod
    async def handle(self, *args, **kwargs):
        raise NotImplementedError("Method 'handle' is not implemented")


class BaseDatabaseHandler(Handler):
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @abstractmethod
    async def handle(self, *args, **kwargs):
        raise NotImplementedError("Method 'handle' is not implemented")
