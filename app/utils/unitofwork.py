from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.purchases_repository import PurchaseRepository
from app.repositories.recommendations_repository import RecommendationRepository
from app.repositories.items_repository import ItemRepository
from app.repositories.user_purchases_repository import UserPurchaseRepository
from app.repositories.users_repository import UserRepository


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

        self.items = ItemRepository(self.session)
        self.recommendations = RecommendationRepository(self.session)
        self.user_purchases = UserPurchaseRepository(self.session)
        self.users = UserRepository(self.session)
        self.purchases = PurchaseRepository(self.session)

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
