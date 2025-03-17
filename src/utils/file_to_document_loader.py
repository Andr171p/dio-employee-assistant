from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from pathlib import Path
    from langchain_core.documents import Document

from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import (
    UnstructuredEmailLoader,
    UnstructuredPowerPointLoader
)


class FileToDocumentLoader:
    def __init__(self, file_path: Union["Path", str]) -> None:
        self._file_path = file_path

    async def load(self) -> List["Document"]:
        extension = self._file_path.split(".")[-1]
        loader = TextLoader(self._file_path)
        if extension == "eml":
            loader = UnstructuredEmailLoader(self._file_path)
        elif extension == "pptx":
            loader = UnstructuredPowerPointLoader(self._file_path)
        documents = await loader.aload()
        return documents
