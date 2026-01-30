import pytest_asyncio

from app.models import User
from app.utils.auth import create_access_token
from app.utils.security import get_password_hash


@pytest_asyncio.fixture
async def setup_database(session_factory):
    # Используем фабрику текущего теста
    async with session_factory() as session:
        user1 = User(
            email="prepair@mail.com",
            name="User",
            password=get_password_hash("password"),
        )
        session.add(user1)
        await session.flush()

        user2 = User(
            email="prepair2@mail.com",
            name="TwoUser",
            password=get_password_hash("password"),
        )
        session.add(user2)

        await session.commit()


@pytest_asyncio.fixture
async def auth_headers(setup_database):
    """Возвращает заголовки с токеном для первого тестового пользователя."""
    token_data = {"sub": "prepair@mail.com"}
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}
