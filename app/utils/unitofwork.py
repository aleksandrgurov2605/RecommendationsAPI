from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.categories import CategoryRepository
from app.repositories.users import UserRepository
from app.repositories.items import ItemRepository
from app.repositories.carts import CartRepository



class IUnitOfWork(ABC):
    rero = None

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.category = CategoryRepository(self.session)
        self.user = UserRepository(self.session)
        self.item = ItemRepository(self.session)
        self.cart = CartRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()
        self.session = None

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()
