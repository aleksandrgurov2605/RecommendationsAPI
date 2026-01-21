from fastapi import APIRouter, status

from app.dependencies.dependencies import UOWDep
from app.schemas.items import ItemCreate, ItemRead
from app.services.items import ItemService

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("/", response_model=list[ItemRead])
async def get_all_items(uow: UOWDep):
    """
    Возвращает список всех активных товаров.
    """
    items = await ItemService.get_all_items(uow)
    return items


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(uow: UOWDep, item: ItemCreate):
    """
    Создаёт новый товар.
    """
    item_created = await ItemService.add_item(uow, item)
    return item_created


@router.get("/{item_id}", response_model=ItemRead)
async def get_item_by_id(uow: UOWDep, item_id: int):
    """
    Возвращает активный товар по id.
    """
    item = await ItemService.get_item(uow, item_id)
    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item(uow: UOWDep, item_id: int, item: ItemCreate):
    """
    Обновляет товар по id.
    """
    item = await ItemService.update_item(uow, item_id, item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(uow: UOWDep, item_id: int):
    """
    Выполняет удаление категории по её ID.
    """
    await ItemService.delete_item(uow, item_id)
    return {"message": f"Item {item_id} was deleted."}
