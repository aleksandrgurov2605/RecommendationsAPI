import pytest_asyncio

from app.models import Category
from app.models.items import Item
from app.models.users import User
from app.utils.auth import create_access_token
from app.utils.security import get_password_hash


@pytest_asyncio.fixture
async def setup_purchase_data(session_factory):
    """Создает пользователя и товары с фиксированным остатком."""
    async with session_factory() as session:
        user = User(
            email="cart_user@mail.com",
            name="CartOwner",
            password=get_password_hash("password"),
        )

        cat = Category(name="Electronics")
        session.add(cat)
        await session.flush()

        # Устанавливаем stock=10
        item1 = Item(
            name="Laptop",
            price=50000,
            category_id=cat.id,
            stock=10,
            is_active=True,
            description="Test Laptop description",
        )
        item2 = Item(
            name="Mouse",
            price=1500,
            category_id=cat.id,
            stock=10,
            is_active=True,
            description="Test Mouse description",
        )

        session.add_all([user, item1, item2])
        await session.commit()
        await session.refresh(user)
        await session.refresh(item2)

        return {"user": user, "item1": item1, "item2": item2}


@pytest_asyncio.fixture
async def purchase_auth_headers(setup_purchase_data):
    user = setup_purchase_data["user"]
    token = create_access_token({"sub": user.email})
    return {"Authorization": f"Bearer {token}"}
