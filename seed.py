import asyncio
import random
from datetime import datetime, timedelta
from decimal import Decimal

import faker_commerce
from faker import Faker
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models import Category, Item, Purchase, PurchaseUnit, User
from app.utils.security import get_password_hash

DATABASE_URL = settings.DATABASE_URL
NUM_USERS = 20
NUM_PARENT_CATEGORIES = 5
NUM_CHILD_CATEGORIES = 10
NUM_ITEMS = 60
NUM_PURCHASES = 500  # Сколько всего чеков создать
MAX_ITEMS_PER_PURCHASE = 10  # Макс. кол-во разных товаров в одном чеке

fake = Faker(["ru_RU"])
fake.add_provider(faker_commerce.Provider)
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine)


async def seed_purchases(session, users, items):
    print(f"Генерация {NUM_PURCHASES} заказов...")
    statuses = ["completed", "pending", "cancelled", "shipped"]

    for _ in range(NUM_PURCHASES):
        user = random.choice(users)
        purchase = Purchase(
            status=random.choice(statuses),
            user_id=user.id,
            total_amount=Decimal("0.00"),
            created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
        )

        num_units = random.randint(1, MAX_ITEMS_PER_PURCHASE)
        selected_items = random.sample(items, num_units)
        current_total = Decimal("0.00")

        for item in selected_items:
            qty = random.randint(1, 3)
            line_total = (item.price * qty).quantize(Decimal("0.00"))

            p_unit = PurchaseUnit(
                item_id=item.id,
                quantity=qty,
                unit_price=item.price,
                total_price=line_total,
                purchase=purchase,
            )
            current_total += line_total
            session.add(p_unit)

        purchase.total_amount = current_total
        session.add(purchase)


async def seed_data():
    async with AsyncSessionLocal() as session:
        try:
            # 1. Очистка и сброс ID
            print("Очистка базы и сброс счетчиков ID...")
            # Порядок в списке важен: от дочерних к родительским
            tables = ["purchase_units", "purchases", "items", "categories", "users"]
            for table in tables:
                await session.execute(
                    text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
                )
            await session.commit()

            print("Начинаю заполнение данными...")

            # 2. Пользователи
            users = [
                User(
                    email=fake.unique.email(),
                    name=fake.name(),
                    password=get_password_hash("qwerty12345"),
                    is_active=True,
                )
                for _ in range(NUM_USERS)
            ]
            session.add_all(users)
            await session.flush()

            # 3. Родительские категории
            parents = [
                Category(name=fake.ecommerce_category(), is_active=True, parent_id=None)
                for _ in range(NUM_PARENT_CATEGORIES)
            ]
            session.add_all(parents)
            await session.flush()

            # 4. Дочерние категории
            children = [
                Category(
                    name=fake.ecommerce_category(),
                    is_active=True,
                    parent_id=random.choice(parents).id,
                )
                for _ in range(NUM_CHILD_CATEGORIES)
            ]
            session.add_all(children)
            await session.flush()

            all_cats = parents + children

            # 5. Товары (реалистичные названия)
            items = [
                Item(
                    name=fake.ecommerce_name(),
                    description=fake.paragraph(nb_sentences=2),
                    price=Decimal(random.uniform(500, 15000)).quantize(Decimal("0.00")),
                    stock=random.randint(0, 100),
                    is_active=True,
                    category_id=random.choice(all_cats).id,
                )
                for _ in range(NUM_ITEMS)
            ]
            session.add_all(items)
            await session.flush()

            # 6. Заказы
            await seed_purchases(session, users, items)

            await session.commit()
            print(
                f"Успех! Создано: {NUM_USERS} юзеров, "
                f"{NUM_ITEMS} товаров и {NUM_PURCHASES} чеков."
            )

        except Exception as e:
            print(f"Критическая ошибка: {e}")
            await session.rollback()
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_data())
