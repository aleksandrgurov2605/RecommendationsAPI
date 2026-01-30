from sqlalchemy import delete, select

from app.models.carts import CartUnit
from app.repositories.base_repository import Repository


class CartRepository(Repository):
    model = CartUnit

    async def get_cart(self, **filter_by: dict):
        """
        Получить корзину пользователя.
        :param filter_by:
        :return:
        """
        current_user_id = filter_by["current_user_id"]

        stmt = (
            select(self.model)
            .where(self.model.user_id == current_user_id)
            .order_by(self.model.id)
        )
        items = await self.session.execute(stmt)
        return items.scalars().all()

    async def get_cart_unit(self, **filter_by):
        """
        Получить запись единицы товара из БД.
        :param filter_by:
        :return:
        """
        user_id = filter_by.get("user_id")
        item_id = filter_by.get("item_id")

        stmt = select(self.model).where(
            self.model.user_id == user_id,
            self.model.item_id == item_id,
        )
        unit = await self.session.execute(stmt)
        return unit.scalar_one_or_none()

    async def delete(self, **filter_by) -> None:
        """
        Удалить запись единицы товара из БД.
        :param filter_by:
        :return:
        """
        user_id = filter_by.get("user_id")
        cart_unit_id = filter_by.get("cart_unit_id")

        stmt = delete(self.model).where(
            self.model.user_id == user_id,
            self.model.id == cart_unit_id,
        )
        await self.session.execute(stmt)

    async def delete_all(self, id: int) -> None:
        """
        Удаляет все единицы товара пользователя из БД. Очищает корзину пользователя.
        :param id:
        :return:
        """
        stmt = delete(self.model).where(self.model.user_id == id)
        await self.session.execute(stmt)
