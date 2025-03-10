from typing import List

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage


def format_docs(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def cut_docs(documents: List[Document], k: int = 5) -> List[Document]:
    documents = documents[:k]
    return documents


def format_chat_history(message_history: List[List[str]]) -> str:
    chat_history = ""
    for message in message_history:
        if isinstance(message, HumanMessage):
            chat_history += f"Пользователь: {message.content}\n"
        elif isinstance(message, AIMessage):
            chat_history += f"Помощник: {message.content}\n"
    return chat_history
