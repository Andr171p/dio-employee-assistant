from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.dialog_model import DialogModel

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declared_attr,
    relationship
)


class DialogRelationMixin:
    _dialog_id_nullable: bool = False
    _dialog_id_unique: bool = False
    _dialog_back_populates: str | None = None

    @declared_attr
    def message_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("dialogs.message_id"),
            unique=cls._dialog_id_unique,
            nullable=cls._dialog_id_nullable
        )

    @declared_attr
    def dialog(cls) -> Mapped["DialogModel"]:
        return relationship(
            "DialogModel",
            back_populates=cls._dialog_back_populates
        )
