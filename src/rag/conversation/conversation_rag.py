from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser
    from langchain_core.runnables import Runnable

from langchain_core.runnables import RunnablePassthrough

from src.rag.base_rag import BaseRAG
from src.rag.rag_utils import format_docs, format_chat_history


class ConversationRAG(BaseRAG):
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

    def _get_chain(self) -> "Runnable":
        chain = (
            {
                "context": self._retriever | format_docs,
                "chat_history": RunnablePassthrough(),
                "question": RunnablePassthrough(),
            } |
            self._prompt |
            self._model |
            self._parser
        )
        return chain

    async def generate(self, query: str, **kwargs) -> str:
        chain = self._get_chain()
        return await chain.ainvoke({"question": query, "chat_history": format_chat_history})
