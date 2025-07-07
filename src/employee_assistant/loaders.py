from pathlib import Path

import pymupdf4llm
from markitdown import MarkItDown, FileConversionException
from src.employee_assistant.document_loaders.docx2markdown import DocxFile, DocxMedia, Converter, DocxFileError

from .base import Document2MarkdownLoader, DocumentLoadingError


class Docx2MarkdownLoader(Document2MarkdownLoader):
    def load(self, file_path: Path | str, **kwargs) -> str:
        use_md_table: bool = kwargs.get("use_md_table", False)
        try:
            docx = DocxFile(str(file_path))
            media = DocxMedia(docx)
            converter = Converter(docx.document(), media, use_md_table)
            return converter.convert()
        except DocxFileError as e:
            raise DocumentLoadingError(f"Error while loading document: {e}") from e


class PDF2MarkdownLoader(Document2MarkdownLoader):
    def load(self, file_path: Path | str, **kwargs) -> str:
        try:
            return pymupdf4llm.to_markdown(str(file_path))
        except Exception as e:
            raise DocumentLoadingError(f"Error while loading document: {e}") from e


class MicrosoftOffice2MarkdownLoader(Document2MarkdownLoader):
    def load(self, file_path: Path | str, **kwargs) -> str:
        try:
            md = MarkItDown()
            result = md.convert(file_path)
            return result.text_content
        except FileConversionException as e:
            raise DocumentLoadingError(f"Error while loading document: {e}") from e
