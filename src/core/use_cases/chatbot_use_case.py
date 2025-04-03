from typing import Optional

from src.core.base import BaseAIAssistant
from src.repository import DialogRepository
from src.handlers import chat_history_saver


class ChatBotUseCase:
    def __init__(
            self,
            ai_assistant: BaseAIAssistant,
            dialog_repository: Optional[DialogRepository]
    ) -> None:
        self._ai_assistant = ai_assistant
        self._dialog_repository = dialog_repository

    @chat_history_saver
    async def answer(self, user_question: str, **kwargs) -> str:
        return await self._ai_assistant.generate(user_question)
