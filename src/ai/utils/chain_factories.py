from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

    from src.ai.rewriter import QueryRewriter
    from src.ai.reranker import CrossEncoderReranker

from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from src.ai.utils.formatters import format_docs, format_messages, cut_messages
from src.ai.chat_memory import RedisChatMemory


def get_chain(
        prompt: "BasePromptTemplate",
        model: "BaseChatModel",
        parser: "BaseTransformOutputParser"
) -> "Runnable":
    chain = prompt | model | parser
    return chain


def get_rag_chain(
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


def get_chat_memory_rag_chain(
        session_id: str,
        retriever: "BaseRetriever",
        prompt: "BasePromptTemplate",
        model: "BaseChatModel",
        parser: "BaseTransformOutputParser"
) -> "Runnable":
    rag_chain = (
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
    return rag_chain


def get_query_rewriter_rag_chain(
        rewriter: "QueryRewriter",
        retriever: "BaseRetriever",
        prompt: "BasePromptTemplate",
        model: "BaseChatModel",
        parser: "BaseTransformOutputParser"
) -> "Runnable":
    rag_chain = (
        {
            "context": RunnablePassthrough() |
                       rewriter |
                       retriever |
                       format_docs,
            "question": RunnablePassthrough()
        } |
        prompt |
        model |
        parser
    )
    return rag_chain


def get_reranker_rag_chain(
        retriever: "BaseRetriever",
        reranker: "CrossEncoderReranker",
        prompt: "BasePromptTemplate",
        model: "BaseChatModel",
        parser: "BaseTransformOutputParser"
) -> "Runnable":
    rag_chain = (
        RunnableParallel({
            "question": RunnablePassthrough(),
            "context": retriever
        })
        .assign(context=reranker | format_docs)
        | prompt
        | model
        | parser
    )
    return rag_chain
