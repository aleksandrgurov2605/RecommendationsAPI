from fastapi import APIRouter, status

from app.dependencies.dependencies import UOWDep
from app.schemas.items import ItemCreate, ItemRead
from app.services.items import ItemService
from app.utils.logger import logger

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("/", response_model=list[ItemRead])
async def get_all_items(uow: UOWDep):
    """
    Получить список всех активных товаров.
    """
    logger.info("Получить список всех активных товаров.")
    items = await ItemService.get_all_items(uow)
    return items


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(uow: UOWDep, item: ItemCreate):
    """
    Создать новый товар.
    """
    logger.info(f"Создать новый товар {item.name}.")
    item_created = await ItemService.add_item(uow, item)
    return item_created


@router.get("/{item_id}", response_model=ItemRead)
async def get_item_by_id(uow: UOWDep, item_id: int):
    """
    Получить активный товар по id.
    """
    logger.info(f"Получить активный товар по id = {item_id}.")
    item = await ItemService.get_item(uow, item_id)
    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item(uow: UOWDep, item_id: int, item: ItemCreate):
    """
    Обновить товар по id
    """
    logger.info(f"Обновить товар по id = {item_id}.")
    item_updated = await ItemService.update_item(uow, item_id, item)
    return item_updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(uow: UOWDep, item_id: int):
    """
    Удалить товар по id.
    """
    logger.info(f"Удалить товар по id {item_id}.")
    await ItemService.delete_item(uow, item_id)
    return {"message": f"Item {item_id} was deleted."}
