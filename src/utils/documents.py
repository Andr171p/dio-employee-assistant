from typing import List

from langchain_core.documents import Document


def format_docs(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def extract_text_from_docs(documents: List[Document]) -> List[str]:
    return [document.page_content for document in documents]
