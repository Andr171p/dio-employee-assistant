from typing import BinaryIO

from src.utils import FileSaver, FileToDocumentLoader
from src.utils.documents import format_docs


class LettersService:
    def __init__(self, file_saver: FileSaver) -> None:
        self._file_saver = file_saver

    async def get_letter(self, letter_file: BinaryIO) -> str:
        file_path = await self._file_saver.save(letter_file)
        loader = FileToDocumentLoader(file_path)
        documents = await loader.load()
        return format_docs(documents)
