import os

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    IS_WINDOWS = os.name == "nt"
    DATABASE_PARAMS = {}
    if IS_WINDOWS:
        DATABASE_PARAMS["poolclass"] = NullPool

engine = create_async_engine(settings.DATABASE_URL, **DATABASE_PARAMS)

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
