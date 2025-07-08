from collections.abc import Iterator

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader


class Office2MdLoader(BaseLoader):
    def __init__(self, doc_path: str | Path) -> None:
        self.doc_path = str(doc_path)

    def lazy_load(self) -> Iterator[Document]:
        try:
            from markitdown import MarkItDown
        except ImportError as ex:
            raise ImportError(
                "Could not import markitdown python package. "
                "Please install it with `pip install markitdown`."
            ) from ex
        md = MarkItDown(enable_plugins=False, docintel_endpoint="<document_intelligence_endpoint>")
        result = md.convert(self.doc_path)
        md_content = result.text_content
        yield Document(page_content=md_content)
