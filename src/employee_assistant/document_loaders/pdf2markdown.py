from typing import Iterator, Optional

import os
import re
import base64
from uuid import uuid4
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter

from .base import ImageMetadata, get_size_by_base64


class Pdf2MdLoader(BaseLoader):
    """Loader for PDF files that converts them to Markdown format.

    Args:
        pdf_path: Path to the PDF file
        include_images: Whether to include images as base64 (default: False)
    """
    def __init__(
            self,
            pdf_path: Path | str,
            include_images: bool = True
    ) -> None:
        self.pdf_path = str(pdf_path)
        self.include_images = include_images
        self.images_temp_dir = f"temp_images_{uuid4()}"

    @property
    def file_name(self) -> str:
        return Path(self.pdf_path).name

    @property
    def file_type(self) -> str:
        return self.file_name.split(".")[-1]

    def lazy_load(self) -> Iterator[Document]:
        try:
            import pymupdf4llm
        except ImportError as ex:
            raise ImportError(
                "Could not import pymupdf4llm python package. "
                "Please install it with `pip install pymupdf4llm`."
            ) from ex
        metadata = {
            "source": self.pdf_path,
            "file_path": self.pdf_path,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "images": []
        }
        if not self.include_images:
            md_text = pymupdf4llm.to_markdown(self.pdf_path)
            yield Document(page_content=md_text, metadata=metadata)
        os.makedirs(self.images_temp_dir)
        md_text = pymupdf4llm.to_markdown(
            self.pdf_path, write_images=self.include_images, image_path=self.images_temp_dir
        )
        metadata["images"] = self._load_images()
        yield Document(page_content=md_text, metadata=metadata)

    def load_and_split(self, text_splitter: Optional[TextSplitter] = None) -> list[Document]:
        text_splitter = text_splitter or RecursiveCharacterTextSplitter()
        documents = self.load()
        if not self.include_images:
            return text_splitter.split_documents(documents)
        chunks: list[Document] = []
        for document in documents:
            texts = text_splitter.split_text(document.page_content)
            images = document.metadata["images"]
            for text in texts:
                file_names = self.__parse_image_file_name(text)
                if not file_names:
                    continue
                in_text_images = [image for image in images if image["src"] in file_names]
                metadata = document.metadata
                metadata["images"] = in_text_images
                chunks.append(Document(page_content=text, metadata=metadata))
        return chunks

    def _load_images(self) -> list[ImageMetadata]:
        images: list[ImageMetadata] = []
        for file_name in os.listdir(self.images_temp_dir):
            file_path = os.path.join(self.images_temp_dir, file_name)
            with open(file_path, "rb") as file:
                data = file.read()
                str_base64 = base64.b64encode(data).decode("utf-8")
                extension = file_name.split(".")[-1]
                size_mb = get_size_by_base64(str_base64)
                images.append(ImageMetadata(
                    src=file_name,
                    source=self.pdf_path,
                    format=extension,
                    size_mb=size_mb,
                    str_base64=str_base64
                ))
            os.remove(file_path)
        os.rmdir(self.images_temp_dir)
        return images

    @staticmethod
    def __parse_image_file_name(md_text: str) -> list[str]:
        pattern = r"!\[(.*?)\]\((.*?)\)"
        matches = re.findall(pattern, md_text)
        return [match.split("/")[-1] for match in matches]
