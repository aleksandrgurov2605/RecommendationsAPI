from fastapi import APIRouter, Query

from app.dependencies.dependencies import UOWDep, UserDep
from app.schemas.purchases import Purchase, PurchaseList
from app.services.purchases import PurchaseService
from app.utils.logger import logger

router = APIRouter(prefix="/purchases", tags=["purchases"])


@router.get("/checkout", response_model=Purchase)
async def checkout_purchase(
    uow: UOWDep,
    current_user: UserDep,
):
    """
    Создать заказ на основе текущей корзины пользователя.
    Сохранить позиции заказа, вычесть остатки и очистить корзину.
    """
    logger.info(
        f"Создать заказ на основе текущей корзины пользователя {current_user.id}"
    )
    result = await PurchaseService.checkout_purchase(uow, current_user)
    return result


@router.get("/", response_model=PurchaseList)
async def list_purchases(
    uow: UOWDep,
    current_user: UserDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """
    Получить все заказы текущего пользователя.
    """
    logger.info(f"Получить все заказы текущего пользователя {current_user.id}.")
    result = await PurchaseService.get_list_purchases(
        uow, current_user, page, page_size
    )
    return result


@router.get("/{purchase_id}", response_model=Purchase)
async def get_purchase(
    purchase_id: int,
    uow: UOWDep,
    current_user: UserDep,
):
    """
    Получить детальную информацию по заказу пользователя.
    """
    logger.info(
        f"Получить детальную информацию по заказу пользователя {current_user.id}."
    )
    result = await PurchaseService.get_purchase(uow, current_user, purchase_id)
    return result
