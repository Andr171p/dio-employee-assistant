from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import BaseModel
from src.database.models.dialog_relation_mixin import DialogRelationMixin


class VoteModel(DialogRelationMixin, BaseModel):
    __tablename__ = "votes"

    _dialog_id_unique = True
    _dialog_back_populates = "vote"

    vote_type: Mapped[str] = mapped_column(
        String,
        CheckConstraint("vote_type IN ('like', 'dislike')")
    )
