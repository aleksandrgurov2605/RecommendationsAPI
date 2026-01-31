from decimal import Decimal

from app.errors.carts_exceptions import CartUnitNotFoundError, NotEnoughItemsError
from app.errors.items_exceptions import ItemHasNoPriceError, ItemNotFoundError
from app.errors.purchases_exceptions import PurchaseNotFoundError
from app.schemas.purchases import Purchase, PurchaseList
from app.schemas.users import UserRead
from app.utils.logger import logger
from app.utils.unitofwork import IUnitOfWork


class PurchaseService:
    @staticmethod
    async def checkout_purchase(
        uow: IUnitOfWork,
        current_user: UserRead,
    ) -> Purchase:
        """
        Создать заказ на основе текущей корзины пользователя.
        Сохранить позиции заказа, вычесть остатки и очистить корзину.
        :param uow:
        :param current_user:
        :return:
        """
        logger.info(
            f"PurchaseService: Создать заказ "
            f"на основе текущей корзины пользователя {current_user.id}."
        )
        async with uow:
            cart_units = await uow.cart.get_cart(current_user_id=current_user.id)
            if not cart_units:
                raise CartUnitNotFoundError
            data = {"status": "Created", "user_id": current_user.id, "total_amount": 0}
            purchase = await uow.purchase.add_one(data)

            total_amount = Decimal("0")

            for cart_unit in cart_units:
                item = cart_unit.item
                if not item or not item.is_active:
                    raise ItemNotFoundError
                if item.stock < cart_unit.quantity:
                    raise NotEnoughItemsError

                unit_price = item.price
                if unit_price is None:
                    raise ItemHasNoPriceError
                total_price = unit_price * cart_unit.quantity
                total_amount += total_price

                data = {
                    "purchase_id": purchase.id,
                    "item_id": cart_unit.item_id,
                    "quantity": cart_unit.quantity,
                    "unit_price": unit_price,
                    "total_price": total_price,
                }
                purchase_unit = await uow.purchase_unit.add_one(data)
                purchase.purchase_units.append(purchase_unit)
                item.stock -= cart_unit.quantity

            purchase.total_amount = total_amount
            data_update = {
                "status": purchase.status,
                "user_id": purchase.user_id,
                "total_amount": purchase.total_amount,
            }
            updated_purchase = await uow.purchase.update(data_update, id=purchase.id)
            if updated_purchase is None:
                raise PurchaseNotFoundError

            await uow.cart.delete_all(current_user.id)
            await uow.commit()
            await uow.refresh(updated_purchase)

            created_purchase = await uow.purchase.fetch_one(id=updated_purchase.id)
            if not created_purchase:
                raise PurchaseNotFoundError

            return Purchase.model_validate(created_purchase)

    @staticmethod
    async def get_list_purchases(
        uow: IUnitOfWork, current_user: UserRead, page: int, page_size: int
    ) -> PurchaseList:
        """
        Получить все заказы текущего пользователя.
        :param page:
        :param page_size:
        :param uow:
        :param current_user:
        :return:
        """
        logger.info(
            f"PurchaseService: Получить все заказы "
            f"текущего пользователя {current_user.id}."
        )
        async with uow:
            purchases = await uow.purchase.get_purchases(
                current_user_id=current_user.id, page=page, page_size=page_size
            )
            total = await uow.purchase.get_count_user_purchases(current_user.id)
            purchases = [Purchase.model_validate(purchase) for purchase in purchases]
            purchase_list = PurchaseList(
                purchases=purchases, total=total[0], page=page, page_size=page_size
            )
        return purchase_list

    @staticmethod
    async def get_purchase(
        uow: IUnitOfWork, current_user: UserRead, purchase_id: int
    ) -> Purchase:
        """
        Получить детальную информацию по заказу пользователя.
        :param purchase_id:
        :param uow:
        :param current_user:
        :return:
        """
        logger.debug(
            f"PurchaseService: Получить детальную информацию "
            f"по заказу пользователя {current_user.id}."
        )
        async with uow:
            purchase_to_return = await uow.purchase.fetch_one(id=purchase_id)
            if not purchase_to_return:
                raise PurchaseNotFoundError
            return Purchase.model_validate(purchase_to_return)
