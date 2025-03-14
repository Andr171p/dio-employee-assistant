from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

from src.ai.rag.base_rag import BaseRAG
from src.ai.chat_memory import save_chat_memory
from src.ai.utils.chain_factories import get_chat_memory_rag_chain


class ChatMemoryRAG(BaseRAG):
    def __init__(
            self,
            retriever: "BaseRetriever",
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser",
    ) -> None:
        self._retriever = retriever
        self._prompt = prompt
        self._model = model
        self._parser = parser

    @save_chat_memory
    async def generate(self, query: str, **kwargs) -> str:
        session_id: str = kwargs.get("session_id")
        rag_chain = get_chat_memory_rag_chain(
            session_id=session_id,
            retriever=self._retriever,
            prompt=self._prompt,
            model=self._model,
            parser=self._parser
        )
        return await rag_chain.ainvoke(query)
