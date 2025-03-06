from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.dialog_model import DialogModel

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    dialogs: Mapped[list["DialogModel"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(user_id={self.user_id}, username={self.username})"

    def __repr__(self) -> str:
        return str(self)