from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.items import ItemRead


class PurchaseUnit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID позиции покупки")
    item_id: int = Field(..., description="ID товара")
    quantity: int = Field(..., ge=1, description="Количество")
    unit_price: Decimal = Field(
        ..., ge=0, description="Цена за единицу на момент покупки"
    )
    total_price: Decimal = Field(..., ge=0, description="Сумма по позиции")
    item: ItemRead | None = Field(None, description="Полная информация о товаре")


class Purchase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID покупки")
    user_id: int = Field(..., description="ID пользователя")
    status: str = Field(..., description="Текущий статус покупки")
    total_amount: Decimal = Field(..., ge=0, description="Общая стоимость")
    created_at: datetime = Field(..., description="Когда покупка была создана")
    updated_at: datetime = Field(..., description="Когда последний раз обновлялась")
    purchase_units: list[PurchaseUnit] = Field(
        default_factory=list, description="Список позиций"
    )


class PurchaseList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    purchases: list[Purchase] = Field(..., description="Заказы на текущей странице")
    total: int = Field(ge=0, description="Общее количество заказов")
    page: int = Field(ge=1, description="Текущая страница")
    page_size: int = Field(ge=1, description="Размер страницы")
