from typing import BinaryIO

from src.ai_agent import BaseAgent
from src.services import LettersService
from src.core.entities import LetterRecommendation


class LettersAssistantUseCase:
    def __init__(
            self,
            ai_agent: BaseAgent,
            letters_service: LettersService
    ) -> None:
        self._ai_agent = ai_agent
        self._letters_service = letters_service

    async def assist(self, letter_file: BinaryIO) -> LetterRecommendation:
        letter = await self._letters_service.get_letter(letter_file)
        recommendations = await self._ai_agent.generate(letter)
        return LetterRecommendation(**recommendations)
