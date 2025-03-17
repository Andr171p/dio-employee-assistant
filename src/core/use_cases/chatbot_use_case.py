from typing import Optional

from src.ai_agents import BaseAIAgent
from src.repository import DialogRepository
from src.decorators import chat_history_saver


class ChatBotUseCase:
    def __init__(
            self,
            ai_agent: BaseAIAgent,
            dialog_repository: Optional[DialogRepository]
    ) -> None:
        self._ai_agent = ai_agent
        self._dialog_repository = dialog_repository

    @chat_history_saver
    async def answer(self, question: str, **kwargs) -> str:
        return await self._ai_agent.generate(question)
