from fastapi import APIRouter, status

from app.dependencies.dependencies import UOWDep
from app.schemas.categories import CategoryCreate, CategoryRead
from app.services.categories import CategoryService
from app.utils.logger import logger

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/", response_model=list[CategoryRead])
async def get_all_categories(uow: UOWDep):
    """
    Получить список всех активных категорий.
    :param uow:
    :return:
    """
    logger.info("Получить список всех активных категорий.")
    categories = await CategoryService.get_all_categories(uow)
    return categories


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(uow: UOWDep, category: CategoryCreate):
    """
    Создать новую категорию.
    :param uow:
    :param category:
    :return:
    """
    logger.info(f"Создать новую категорию {category.name}.")
    category_created = await CategoryService.add_category(uow, category)
    return category_created


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category_by_id(uow: UOWDep, category_id: int):
    """
    Получить активную категорию по id.
    :param uow:
    :param category_id:
    :return:
    """
    logger.info(f"Получить активную категорию по id = {category_id}.")
    category = await CategoryService.get_category(uow, category_id)
    return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(uow: UOWDep, category_id: int, category: CategoryCreate):
    """
    Обновить категорию по id.
    :param uow:
    :param category_id:
    :param category:
    :return:
    """
    logger.info(f"Обновить категорию по id {category_id}.")
    category_updated = await CategoryService.update_category(uow, category_id, category)
    return category_updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(uow: UOWDep, category_id: int):
    """
    Удалить категорию по id.
    :param uow:
    :param category_id:
    :return:
    """
    logger.info(f"Удалить категорию по id {category_id}.")
    await CategoryService.delete_category(uow, category_id)
    return {"message": f"Category {category_id} was deleted."}
