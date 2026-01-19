from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    name: str


class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
