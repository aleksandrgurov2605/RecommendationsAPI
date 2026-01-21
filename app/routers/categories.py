from fastapi import APIRouter, status

from app.dependencies.dependencies import UOWDep
from app.schemas.categories import CategoryCreate, CategoryRead
from app.services.categories import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/", response_model=list[CategoryRead])
async def get_all_categories(uow: UOWDep):
    """
    Возвращает список всех активных категорий.
    """
    categories = await CategoryService.get_all_categories(uow)
    return categories


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(uow: UOWDep, category: CategoryCreate):
    """
    Создаёт новую категорию.
    """
    category_created = await CategoryService.add_category(uow, category)
    return category_created


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category_by_id(uow: UOWDep, category_id: int):
    """
    Возвращает активную категорию по id.
    """
    category = await CategoryService.get_category(uow, category_id)
    return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(uow: UOWDep, category_id: int, category: CategoryCreate):
    """
    Обновляет категорию по id.
    """
    category = await CategoryService.update_category(uow, category_id, category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(uow: UOWDep, category_id: int):
    """
    Выполняет удаление категории по id.
    """
    await CategoryService.delete_category(uow, category_id)
    return {"message": f"Category {category_id} was deleted."}
