import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.main import app as prod_app
from app.models import (
    Category,  # noqa
    User,  # noqa
)
from app.utils.unitofwork import UnitOfWork

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # отдельная БД для тестов


@pytest_asyncio.fixture
async def session_factory():
    # Генерируем уникальное имя БД для каждого теста, чтобы память не пересекалась
    # test_db_url = f"sqlite+aiosqlite:///file:{uuid.uuid4()}?mode=memory&cache=shared"

    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield factory
    await engine.dispose()


@pytest_asyncio.fixture
async def client(session_factory):
    async def get_uow_test():
        uow = UnitOfWork()
        uow.session_factory = session_factory  # Инъекция фабрики ТЕКУЩЕГО теста
        return uow

    prod_app.dependency_overrides[UnitOfWork] = get_uow_test

    transport = ASGITransport(app=prod_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c

    prod_app.dependency_overrides.clear()
