from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser
    from langchain_core.runnables import Runnable

from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

from src.rag.base_rag import BaseRAG
from src.rag.rag_utils import format_docs
from src.rag.memory.chat_history_factory import ChatHistoryFactory


class MemoryRAG(BaseRAG):
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
                "question": RunnablePassthrough(),
            } |
            self._prompt |
            self._model |
            self._parser
        )
        return chain

    async def generate(self, query: str, **kwargs) -> str:
        session_id: str = kwargs.get("session_id")
        chat_history_factory = kwargs.get("chat_history_factory")
        chain = self._get_chain()
        chain_with_history = RunnableWithMessageHistory(
            chain, chat_history_factory.get_or_create_chat_history,
            input_messages_key="question",
            history_key="chat_history",
            output_messages_key="answer",
        )
        return await chain_with_history.ainvoke({"question": query}, config={"configurable": {"session_id": session_id}})
