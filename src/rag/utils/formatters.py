from typing import List, Dict

from langchain_core.documents import Document


def format_docs(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def cut_docs(documents: List[Document], k: int = 5) -> List[Document]:
    documents = documents[:k]
    return documents


def format_messages(messages: List[Dict]) -> str:
    return "\n".join([f"{message['type']}: {message['content']}" for message in messages])


def cut_messages(messages: List[Dict], k: int = 3) -> List[Dict]:
    return messages[:k]
