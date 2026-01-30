from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(
        min_length=3, max_length=50, description="Название категории (3-50 символов)"
    )
    parent_id: int | None = Field(
        default=None, description="ID родительской категории, если есть"
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Уникальный идентификатор категории")
    is_active: bool = Field(description="Активность категории")
