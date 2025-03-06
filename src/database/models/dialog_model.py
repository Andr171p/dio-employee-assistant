from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.vote_model import VoteModel

from sqlalchemy import Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import BaseModel
from src.database.models.user_relation_mixin import UserRelationMixin


class DialogModel(UserRelationMixin, BaseModel):
    __tablename__ = "dialogs"

    _user_back_populates = "dialogs"

    user_message: Mapped[str] = mapped_column(Text)
    chat_bot_message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    vote: Mapped["VoteModel"] = relationship(back_populates="dialog")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(user_id={self.user_id}, user_message={self.user_message}, chat_bot_message={self.chat_bot_message}, created_at={self.created_at})"

    def __repr__(self) -> str:
        return str(self)
