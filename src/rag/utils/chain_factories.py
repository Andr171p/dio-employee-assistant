from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

from langchain_core.runnables import RunnablePassthrough

from src.rag.utils.formatters import format_docs, format_messages, cut_messages
from src.rag.chat_memory import RedisChatMemory


def get_naive_rag_chain(
        retriever: "BaseRetriever",
        prompt: "BasePromptTemplate",
        model: "BaseChatModel",
        parser: "BaseTransformOutputParser"
) -> "Runnable":
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        } |
        prompt |
        model |
        parser
    )
    return chain


def get_conversation_rag_chain(
        session_id: str,
        retriever: "BaseRetriever",
        prompt: "BasePromptTemplate",
        model: "BaseChatModel",
        parser: "BaseTransformOutputParser"
) -> "Runnable":
    chain = (
        {
            "context": RedisChatMemory(session_id) |
                       cut_messages |
                       format_messages |
                       retriever |
                       format_docs,
            "question": RunnablePassthrough()
        } |
        prompt |
        model |
        parser
    )
    return chain
