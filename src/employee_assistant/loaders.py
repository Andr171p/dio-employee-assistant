from pathlib import Path

import pymupdf4llm
from markitdown import MarkItDown, FileConversionException
from docx2md import DocxFile, DocxMedia, Converter, DocxFileError

from .base import Document2MarkdownLoader, DocumentLoadingError


class Docx2MarkdownLoader(Document2MarkdownLoader):
    def load(self, file_path: Path | str, **kwargs) -> str:
        use_md_table: bool = kwargs.get("use_md_table", False)
        try:
            docx = DocxFile(str(file_path))
            media = DocxMedia(docx)
            converter = Converter(docx.document(), media, use_md_table)
            md_text = converter.convert()
            return md_text
        except DocxFileError as e:
            raise DocumentLoadingError(f"Error while loading document: {e}") from e


class PDF2MarkdownLoader(Document2MarkdownLoader):
    def load(self, file_path: Path | str, **kwargs) -> str:
        try:
            md_text = pymupdf4llm.to_markdown(str(file_path))
            return md_text
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
