import os
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import settings

IS_WORKER = os.getenv("IS_CELERY_WORKER") == "True"

DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS: dict[str, Any] = {"pool_size": 10, "max_overflow": 20}

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
elif IS_WORKER:
    DATABASE_PARAMS = {"poolclass": NullPool}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"{self.__class__.__name__}({', '.join(cols)})"


async def get_async_session():
    async with async_session_maker() as session:
        yield session
