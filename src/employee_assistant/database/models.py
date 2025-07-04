from sqlalchemy import Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MessageOrm(Base):
    __tablename__ = "messages"

    role: Mapped[str]
    chat_id: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    grade: Mapped[str | None] = mapped_column(nullable=True)

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", "check_message_role"),
    )
