from src.rag import BaseRAG


class ChatBotUseCase:
    def __init__(self, rag: BaseRAG):
        self._rag = rag

    async def answer(self, question: str) -> str:
        return await self._rag.generate(question)
