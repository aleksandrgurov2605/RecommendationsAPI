from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar, Generic, Sequence

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base

T = TypeVar("T", bound=Base)


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def add_one(self, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_one(self, **filter_by: Any) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: dict, id: Any) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: Any) -> None:
        raise NotImplementedError


class Repository(AbstractRepository[T]):
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> T:
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

    async def fetch_one(self, **filter_by: Any) -> T | None:
        """
        Получить одну запись по id или None
        :param filter_by:
        :return:
        """
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, data: dict, id: Any) -> T | None:
        """
        Обновить одну запись по условию filter_by данными из data.
        :param data:
        :param id:
        :return:
        """
        stmt = (
            update(self.model)
            .filter_by(id=id)
            .values(data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, id: Any) -> None:
        """
        Удалить одну запись из БД по условию filter_by.
        :param id:
        :return:
        """
        stmt = delete(self.model).filter_by(id=id)
        await self.session.execute(stmt)
