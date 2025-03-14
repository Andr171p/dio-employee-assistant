from typing import Optional

from src.ai.rag import BaseRAG
from src.repository import DialogRepository
from src.utils import chat_history_saver


class ChatBotUseCase:
    def __init__(
            self,
            rag: BaseRAG,
            dialog_repository: Optional[DialogRepository]
    ) -> None:
        self._rag = rag
        self._dialog_repository = dialog_repository

    @chat_history_saver
    async def answer(self, question: str, **kwargs) -> str:
        user_id = str(kwargs.get("user_id"))
        return await self._rag.generate(question, session_id=user_id)
