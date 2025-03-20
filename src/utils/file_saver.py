import uuid
from typing import BinaryIO

from src.misc.file_writers import write_eml
from src.config import BASE_DIR


class FileSaver:
    def __init__(self) -> None:
        self.directory = BASE_DIR / "letters"

    async def save(self, binary_file: BinaryIO) -> str:
        file_name = f"{uuid.uuid4()}.eml"
        file_path = self.directory / file_name
        await write_eml(file_path, binary_file)
        return file_path
