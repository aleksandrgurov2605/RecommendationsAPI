from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.items import ItemRead



class Purchase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID покупки")
    user_id: int = Field(..., description="ID пользователя")
    status: str = Field(..., description="Текущий статус покупки")
    total_amount: Decimal = Field(..., ge=0, description="Общая стоимость")
    created_at: datetime = Field(..., description="Когда покупка была создана")
    updated_at: datetime = Field(..., description="Когда последний раз обновляась")
    purchase_items: list[PurchaseItem] = Field(default_factory=list, description="Список позиций")

class PurchaseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID позиции покупки")
    item_id: int = Field(..., description="ID товара")
    quantity: int = Field(..., ge=1, description="Количество")
    unit_price: Decimal = Field(..., ge=0, description="Цена за единицу на момент покупки")
    total_price: Decimal = Field(..., ge=0, description="Сумма по позиции")
    item: ItemRead | None = Field(None, description="Полная информация о товаре")