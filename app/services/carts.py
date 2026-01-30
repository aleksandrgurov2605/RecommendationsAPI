from decimal import Decimal

from app.errors.carts_exceptions import CartUnitNotFoundError
from app.errors.items_exceptions import ItemNotFoundError
from app.schemas.carts import CartUnitRead, CartUnitUpdate, Cart, CartUnitCreate
from app.schemas.users import UserRead
from app.utils.unitofwork import IUnitOfWork


class CartService:
    @staticmethod
    async def add_item_to_cart(
            uow: IUnitOfWork,
            current_user: UserRead,
            cart_unit: CartUnitCreate
    ) -> CartUnitRead:
        """
        Добавить товар в корзину.
        :param uow:
        :param current_user:
        :param cart_unit:
        :return:
        """
        async with uow as uow:
            item = await uow.item.get_active_item(item_id=cart_unit.item_id)
            if not item:
                raise ItemNotFoundError
            cart_unit_from_db = await uow.cart.get_cart_unit(user_id=current_user.id, item_id=cart_unit.item_id)
            if cart_unit_from_db:
                cart_unit_from_db.quantity += cart_unit.quantity
            else:
                data = dict(user_id=current_user.id, item_id=cart_unit.item_id, quantity=cart_unit.quantity)
                cart_unit_from_db = await uow.cart.add_one(data)
            unit_to_return = CartUnitRead.model_validate(cart_unit_from_db)
            await uow.commit()
        return unit_to_return

    @staticmethod
    async def get_cart(
            uow: IUnitOfWork,
            current_user: UserRead
    ) -> Cart:
        """
        Получить корзину пользователя.
        :param uow:
        :param current_user:
        :return:
        """
        async with uow as uow:
            units = await uow.cart.get_cart(current_user_id=current_user.id)
            units = [CartUnitRead.model_validate(unit) for unit in units]

        total_quantity = sum(unit.quantity for unit in units)
        price_units = (
            Decimal(unit.quantity) *
            (Decimal(unit.item.price) if unit.item.price is not None else Decimal("0"))
            for unit in units
        )
        total_price_decimal = sum(price_units, Decimal("0"))

        return Cart(
            user_id=current_user.id,
            units=units,
            total_quantity=total_quantity,
            total_price=total_price_decimal
        )

    @staticmethod
    async def update_cart_unit(
            item_id: int,
            uow: IUnitOfWork,
            current_user: UserRead,
            cart_unit: CartUnitUpdate
    ) -> CartUnitRead:
        """
        Обновить единицу корзины.
        :param item_id:
        :param uow:
        :param current_user:
        :param cart_unit:
        :return:
        """
        async with uow as uow:
            item = await uow.item.get_active_item(item_id=item_id)
            if not item:
                raise ItemNotFoundError
            cart_unit_from_db = await uow.cart.get_cart_unit(user_id=current_user.id, item_id=item_id)
            if not cart_unit_from_db:
                raise CartUnitNotFoundError
            cart_unit_from_db.quantity = cart_unit.quantity
            await uow.commit()

            cart_unit_from_db = await uow.cart.get_cart_unit(user_id=current_user.id, item_id=item_id)
            cart_unit_to_return = CartUnitRead.model_validate(cart_unit_from_db)
            return cart_unit_to_return

    @staticmethod
    async def delete_cart_unit(
            uow: IUnitOfWork,
            current_user: UserRead,
            cart_unit_id: int
    ) -> None:
        """
        Удалить единицу корзины.
        :param uow:
        :param current_user:
        :param cart_unit_id:
        :return:
        """
        async with uow as uow:
            existing_cart_unit = await uow.cart.fetch_one(id=cart_unit_id)
            if not existing_cart_unit:
                raise CartUnitNotFoundError

            await uow.cart.delete(user_id=current_user.id, cart_unit_id=cart_unit_id)
            await uow.commit()

    @staticmethod
    async def delete_all_cart_units(
            uow: IUnitOfWork,
            current_user: UserRead
    ) -> None:
        """
        Очистить корзину пользователя.
        :param uow:
        :param current_user:
        :return:
        """
        async with uow as uow:
            await uow.cart.delete_all(id=current_user.id)
            await uow.commit()
