from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    purchases: Mapped["Purchase"] = relationship("Purchase",
                                        back_populates="user")
