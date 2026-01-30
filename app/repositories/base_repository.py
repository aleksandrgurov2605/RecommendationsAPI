from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base


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
    async def update(self, data: dict, id: Any) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: Any):
        raise NotImplementedError


class Repository(AbstractRepository):
    model: Type[Base] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> BaseModel:
        """
        Добавить одну запись в БД.
        :param data:
        :return:
        """
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        """
        Получить все записи из таблицы в БД, списком
        :return:
        """
        res = await self.session.execute(select(self.model))
        return res.scalars().all()

    async def fetch_one(self, id: int) -> BaseModel | None:
        """
        Получить одну запись по id или None
        :param id:
        :return:
        """
        stmt = select(self.model).where(self.model.id==id)
        res  = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, data: dict, id: int) -> BaseModel | None:
        """
        Обновить одну запись по условию filter_by данными из data.
        :param data:
        :param id:
        :return:
        """
        stmt = update(self.model).where(self.model.id==id).values(data).returning(self.model)
        data = await self.session.execute(stmt)
        res = data.scalar_one()

        return res

    async def delete(self, id: int) -> None:
        """
        Удалить одну запись из БД по условию filter_by.
        :param id:
        :return:
        """
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)

