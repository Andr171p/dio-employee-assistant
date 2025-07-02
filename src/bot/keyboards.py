from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..schemas import Grade


class GradeCallback(CallbackData, prefix="grade"):
    message_id: int
    grade: Grade


def grade_kb(message_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👍", callback_data=GradeCallback(message_id=message_id, grade=Grade.LIKE))
    builder.button(text="👎", callback_data=GradeCallback(message_id=message_id, grade=Grade.DISLIKE))
    return builder.as_markup()
