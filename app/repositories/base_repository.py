from abc import ABC, abstractmethod
from typing import Any, TypeVar, Type

from pydantic import BaseModel

from sqlalchemy import CursorResult, func, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_one(self, **filter_by: Any) -> BaseModel | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: dict, where: Any) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, where: Any):
        raise NotImplementedError


class Repository(AbstractRepository):
    model: Type[Any] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> BaseModel:
        """Добавить одну запись в БД (модель Pydentic)"""

        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        """Получить все записи из таблицы в БД, списком"""

        res = await self.session.execute(select(self.model))
        return res.scalars().all()

    async def fetch_one(self, where: int) -> BaseModel | None:
        """Получить одну запись, по условию where, или None"""

        stmt = select(self.model).where(self.model.id==where)
        res  = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, data: dict, where: int) -> BaseModel | None:
        """Обновляет одну запись данными из data, по условию filter_by."""

        stmt = update(self.model).where(self.model.id==where).values(data).returning(self.model)
        data = await self.session.execute(stmt)
        res = data.scalar_one()

        return res

    async def delete(self, where: int) -> None:
        """Удаляет одну запись из БД по условию filter_by."""

        stmt = delete(self.model).where(self.model.id == where)
        await self.session.execute(stmt)

