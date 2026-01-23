from fastapi import APIRouter, status, Response

from app.dependencies.dependencies import UOWDep, UserDep
from app.schemas.carts import Cart, CartUnitCreate, CartUnitRead, CartUnitUpdate

from app.services.carts import CartService
from app.utils.logger import logger

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)


@router.get("/", response_model=Cart)
async def get_cart(
        uow: UOWDep,
        current_user: UserDep,
):
    """
    Получить корзину пользователя.
    :param uow:
    :param current_user:
    :return:
    """
    logger.info(f"Получить корзину пользователя.")
    result = await CartService.get_cart(uow, current_user)
    return result


@router.post("/units", response_model=CartUnitRead, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
        payload: CartUnitCreate,
        uow: UOWDep,
        current_user: UserDep
):
    """
    Добавить товар в корзину.
    :param payload:
    :param uow:
    :param current_user:
    :return:
    """
    logger.info(f"Добавить товар {payload.item_id} в корзину.")
    cart_item = await CartService.add_item_to_cart(uow, current_user, payload)
    return cart_item


@router.put("/units/{item_id}", response_model=CartUnitRead)
async def update_cart_unit(
        item_id: int,
        payload: CartUnitUpdate,
        uow: UOWDep,
        current_user: UserDep
):
    """
    Обновить количество товара в корзине.
    :param item_id:
    :param payload:
    :param uow:
    :param current_user:
    :return:
    """
    logger.info(f"Обновить количество товара {payload.item_id} в корзине.")
    updated_unit = await CartService.update_cart_unit(item_id, uow, current_user, payload)
    return updated_unit


@router.delete("/units/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_unit_from_cart(
        cart_unit_id: int,
        uow: UOWDep,
        current_user: UserDep
):
    """
    Удалить товар из корзины.
    :param cart_unit_id:
    :param uow:
    :param current_user:
    :return:
    """
    logger.info(f"Удалить товар {cart_unit_id=} в корзины.")
    await CartService.delete_cart_unit(uow, current_user, cart_unit_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
        uow: UOWDep,
        current_user: UserDep
):
    """
    Удалить все товары из корзины.
    :param uow:
    :param current_user:
    :return:
    """
    logger.info(f"Удалить все товары из корзины пользователя {current_user.id}.")
    await CartService.delete_all_cart_units(uow, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


