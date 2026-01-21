import pytest_asyncio

from app.models import User


@pytest_asyncio.fixture
async def setup_database(session_factory):
    # Используем фабрику текущего теста
    async with session_factory() as session:
        user1 = User(email="fake_email_prepair@fakemail.com", name="User", password="password")
        session.add(user1)
        await session.flush()  # Получаем ID

        user2 = User(email="fake_email_prepair2@fakemail.com", name="TwoUser", password="password")
        session.add(user2)

        await session.commit()
