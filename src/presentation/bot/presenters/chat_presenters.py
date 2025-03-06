from aiogram.types import Message

from src.presentation.bot.presenters.base_presenter import BasePresenter


class ChatBotAnswerPresenter(BasePresenter):
    @classmethod
    async def present(cls, message: Message, **kwargs) -> None:
        answer: str = kwargs.get("answer")
        await message.answer(answer)
