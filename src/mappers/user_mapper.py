from aiogram.types import Message

from src.core.entities import User


class UserMapper:
    @staticmethod
    def from_message(message: Message) -> User:
        return User(
            user_id=message.from_user.id,
            username=message.from_user.username,
        )
