from typing import Optional

from src.rag import BaseRAG
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
        return await self._rag.generate(question)
