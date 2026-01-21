import pytest_asyncio

from app.models import Category


@pytest_asyncio.fixture
async def setup_database(session_factory):
    # Используем фабрику текущего теста
    async with session_factory() as session:
        category1 = Category(name="Электроника", parent_id=None)
        session.add(category1)
        await session.flush()  # Получаем ID

        category2 = Category(name="Смартфоны", parent_id=category1.id)
        session.add(category2)

        await session.commit()

