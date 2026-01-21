from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    name: str = Field(min_length=2, max_length=40, description="Имя пользователя(2-40 символов)")


class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
