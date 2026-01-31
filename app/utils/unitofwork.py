from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.database import async_session_maker
from app.repositories.carts import CartRepository
from app.repositories.categories import CategoryRepository
from app.repositories.items import ItemRepository
from app.repositories.purchases import PurchaseRepository, PurchaseUnitRepository
from app.repositories.recommendations import RecommendationRepository
from app.repositories.users import UserRepository
from app.utils.logger import logger


class IUnitOfWork(ABC):
    rero = None
    category: CategoryRepository
    user: UserRepository
    item: ItemRepository
    cart: CartRepository
    purchase: PurchaseRepository
    purchase_unit: PurchaseUnitRepository
    recommendation: RecommendationRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def flush(self): ...

    @abstractmethod
    async def refresh(self, instance, attribute_names=None): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):
    session: AsyncSession | None

    def __init__(self):
        self.session_factory: async_sessionmaker[AsyncSession] = async_session_maker
        self.session = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_factory()

        if self.session is not None:
            self.category = CategoryRepository(self.session)
            self.user = UserRepository(self.session)
            self.item = ItemRepository(self.session)
            self.cart = CartRepository(self.session)
            self.purchase = PurchaseRepository(self.session)
            self.purchase_unit = PurchaseUnitRepository(self.session)
            self.recommendation = RecommendationRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.rollback()
        except Exception as rollback_exc:
            logger.error(f"Rollback failed: {rollback_exc}")
        finally:
            if self.session:
                await self.session.close()
                self.session = None

    async def commit(self):
        if self.session:
            await self.session.commit()

    async def flush(self):
        if self.session:
            await self.session.flush()

    async def refresh(self, instance, attribute_names=None):
        if self.session:
            await self.session.refresh(instance, attribute_names)

    async def rollback(self):
        if self.session:
            await self.session.rollback()
