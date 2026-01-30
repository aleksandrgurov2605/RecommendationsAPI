import pytest_asyncio

from app.models import Category, Item

items = [
    {
        "name": "iPhone 17",
        "description": "The iPhone 17 features a 6.3-inch ProMotion OLED display",
        "price": 799,
        "stock": 10,
        "category_id": 2,
    },
    {
        "name": "Galaxy S25 Ultra",
        "description": "The Samsung Galaxy S25 Ultra",
        "price": 900,
        "stock": 13,
        "category_id": 2,
    },
]


@pytest_asyncio.fixture
async def setup_database(session_factory):
    # Используем фабрику текущего теста
    async with session_factory() as session:
        category1 = Category(name="Электроника", parent_id=None)
        session.add(category1)
        await session.flush()  # Получаем ID

        category2 = Category(name="Смартфоны", parent_id=category1.id)
        session.add(category2)

        await session.flush()

        item1 = Item(**items[0])
        session.add(item1)

        item2 = Item(**items[1])
        session.add(item2)

        await session.commit()
