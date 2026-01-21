from fastapi import APIRouter, status

from app.dependencies.dependencies import UOWDep
from app.schemas.users import UserCreate, UserRead
from app.services.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserRead])
async def get_all_users(uow: UOWDep):
    """
    Возвращает список всех активных пользователей.
    """
    categories = await UserService.get_all_users(uow)
    return categories


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(uow: UOWDep, user: UserCreate):
    """
    Создаёт нового пользователя.
    """
    user_created = await UserService.add_user(uow, user)
    return user_created


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(uow: UOWDep, user_id: int):
    """
    Возвращает активного пользователя по id.
    """
    user = await UserService.get_user(uow, user_id)
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(uow: UOWDep, user_id: int, user: UserCreate):
    """
    Обновляет пользователя по id.
    """
    user = await UserService.update_user(uow, user_id, user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(uow: UOWDep, user_id: int):
    """
    Выполняет удаление пользователя по id.
    """
    await UserService.delete_user(uow, user_id)
    return {"message": f"User {user_id} was deleted."}
