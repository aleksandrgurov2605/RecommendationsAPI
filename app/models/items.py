from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.carts import CartUnit
    from app.models.categories import Category
    from app.models.purchases import PurchaseUnit


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    category: Mapped["Category"] = relationship(  # noqa: F821
        "Category",  # noqa: F821
        back_populates="items",
    )
    purchase_unit: Mapped[list["PurchaseUnit"]] = relationship(  # noqa: F821
        "PurchaseUnit",  # noqa: F821
        back_populates="item",
    )

    cart_units: Mapped[list["CartUnit"]] = relationship(  # noqa: F821
        "CartUnit",  # noqa: F821
        back_populates="item",
    )
