from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.items import ItemRead


class CartUnitBase(BaseModel):
    item_id: int = Field(description="ID товара")
    quantity: int = Field(ge=1, description="Количество товара")


class CartUnitCreate(CartUnitBase):
    pass


class CartUnitUpdate(BaseModel):
    quantity: int = Field(..., ge=1, description="Новое количество товара")


class CartUnitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID позиции корзины")
    user_id: int = Field(description="ID пользователя")
    quantity: int = Field(..., ge=1, description="Количество товара")
    item: ItemRead = Field(..., description="Информация о товаре")




class Cart(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(..., description="ID пользователя")
    units: list[CartUnitRead] = Field(default_factory=list, description="Содержимое корзины")
    total_quantity: int = Field(..., ge=0, description="Общее количество товаров")
    total_price: Decimal = Field(..., ge=0, description="Общая стоимость товаров", examples=[Decimal("250.00")])

