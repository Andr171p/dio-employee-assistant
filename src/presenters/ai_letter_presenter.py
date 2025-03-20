from aiogram.types import Message

from src.core.entities import AILetter


class AILetterPresenter:
    def __init__(self, message: Message) -> None:
        self.message = message

    async def present(self, ai_letter: AILetter) -> None:
        await self.message.answer(text=ai_letter.critique)
        await self.message.answer(text=ai_letter.rewritten_letter)
