from typing import Optional, Union

from src.core.base import BaseAI
from src.repository import DialogRepository
from src.decorators import chat_history_saver


class ChatBotUseCase:
    def __init__(
            self,
            ai_assistant: BaseAI,
            dialog_repository: Optional[DialogRepository]
    ) -> None:
        self._ai_assistant = ai_assistant
        self._dialog_repository = dialog_repository

    @chat_history_saver
    async def answer(self, question: str, **kwargs) -> str:
        return await self._ai_assistant.generate(question)
