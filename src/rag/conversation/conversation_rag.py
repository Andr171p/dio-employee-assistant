from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

from langchain_core.runnables import RunnablePassthrough

from src.rag.base_rag import BaseRAG
from src.rag.rag_utils import format_docs, format_messages
from src.rag.conversation.redis_chat_memory import RedisChatMemory


class ConversationRAG(BaseRAG):
    def __init__(
            self,
            retriever: "BaseRetriever",
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser",
    ) -> None:
        self._chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
                "chat_history": RunnablePassthrough(),
            } |
            prompt |
            model |
            parser
        )

    async def generate(self, query: str, **kwargs) -> str:
        session_id: str = kwargs.get("session_id")
        memory = RedisChatMemory(session_id)
        messages = memory.get_messages()
        response = await self._chain.ainvoke(query, chat_history=format_messages(messages))
        memory.add_message({"type": "human", "content": query})
        memory.add_message({"type": "ai", "content": response})
        return response

