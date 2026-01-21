from decimal import Decimal

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal]
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    category: Mapped["Category"] = relationship("Category",
                                                      back_populates="items")
    purchase_unit: Mapped[list["PurchaseUnit"]] = relationship("PurchaseUnit",
                                        back_populates="item")