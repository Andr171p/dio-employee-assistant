from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

from langgraph.graph.message import add_messages


class RAGState(TypedDict):
    """Состояние RAG агента"""
    messages: Annotated[Sequence[BaseMessage], add_messages]  # Сообщения пользователя
    question: str                                             # Вопрос пользователя
    documents: list[Document]                                 # Найденные документы
