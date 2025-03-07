from typing import List

from langchain_core.documents import Document


def format_docs(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def cut_docs(documents: List[Document], k: int = 5) -> List[Document]:
    documents = documents[:k]
    return documents
