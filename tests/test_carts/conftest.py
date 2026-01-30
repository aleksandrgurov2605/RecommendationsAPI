import pytest_asyncio
from app.models import User, Item, Category
from app.utils.auth import create_access_token
from app.utils.security import get_password_hash


@pytest_asyncio.fixture
async def setup_cart_db(session_factory):
    async with session_factory() as session:
        # 1. Создаем пользователя
        user = User(email="cart_user@mail.com", name="CartOwner", password=get_password_hash("password"))
        session.add(user)

        # 2. Создаем категорию и товары
        cat = Category(name="Electronics")
        session.add(cat)
        await session.flush()

        item1 = Item(
            name="Phone",
            price=1000,
            category_id=cat.id,
            stock=10,
            description="Test phone description"
        )
        item2 = Item(
            name="Laptop",
            price=2000,
            category_id=cat.id,
            stock=10,
            description="Test laptop description"
        )
        session.add_all([item1, item2])

        await session.commit()
        return {"user": user, "item1": item1, "item2": item2}


@pytest_asyncio.fixture
async def cart_auth_headers(setup_cart_db):
    token = create_access_token({"sub": "cart_user@mail.com"})
    return {"Authorization": f"Bearer {token}"}
