from typing import BinaryIO

from src.core.base import BaseAIAssistant
from src.services import LettersService
from src.core.entities import AILetter


class LettersAssistantUseCase:
    def __init__(
            self,
            ai_assistant: BaseAIAssistant,
            letters_service: LettersService
    ) -> None:
        self._ai_assistant = ai_assistant
        self._letters_service = letters_service

    async def assist(self, letter_file: BinaryIO) -> AILetter:
        letter = await self._letters_service.get_letter(letter_file)
        generated = await self._ai_assistant.generate(letter)
        return AILetter(**generated)
