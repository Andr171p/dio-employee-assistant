from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def votes_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="👍", callback_data="vote_like"),
        InlineKeyboardButton(text="👎", callback_data="vote_dislike")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
