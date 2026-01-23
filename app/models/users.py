from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    purchases: Mapped[list["Purchase"]] = relationship("Purchase",
                                                       back_populates="user")
    cart_units: Mapped[list["CartUnit"]] = relationship("CartUnit",
                                                        back_populates="user")
