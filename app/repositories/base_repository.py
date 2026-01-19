from abc import ABC, abstractmethod
import logging
from typing import Any
from pydantic import BaseModel

from sqlalchemy import CursorResult, func, select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_one(self, **filter_by: dict) -> BaseModel | None:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, data: BaseModel, **where: dict) -> BaseModel:
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> BaseModel:
        """Добавить одну запись в БД (модель Pydentic)"""

        stmt = insert(self.model).values(**data).returning(self.model)
        data = await self.session.execute(stmt)
        res = data.scalar_one()
        return res

    async def find_all(self):
        """Получить все записи из таблицы в БД, списком"""

        data = await self.session.execute(select(self.model))
        result = data.scalars().all()
        return result

    async def fetch_one(self, **filter_by: dict) -> BaseModel | None:
        """Получить одну запись, по условию filter_by, или None"""

        stmt = select(self.model).filter_by(**filter_by)
        data = (await self.session.execute(stmt)).scalar_one_or_none()

        return data

    async def update_one(self, data: BaseModel, **where: dict) -> BaseModel:
        """Обновляет одну запись данными из data, по условию where. Если запись не одна, вызывается исключение"""

        stmt = update(self.model).values(**data).where(**where).returning(self.model)
        data = await self.session.execute(stmt)
        result = data.scalar_one().to_pydantic_model()

        return result
