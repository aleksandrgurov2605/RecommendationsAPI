from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.purchases import Purchase
    from app.models.carts import CartUnit

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    purchases: Mapped[list["Purchase"]] = relationship(  # noqa: F821
        "Purchase",  # noqa: F821
        back_populates="user",
    )
    cart_units: Mapped[list["CartUnit"]] = relationship(  # noqa: F821
        "CartUnit",  # noqa: F821
        back_populates="user",
    )
