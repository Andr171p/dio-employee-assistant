import base64
from pathlib import Path

from docx import Document

from src.employee_assistant.base import ImageExtractor
from src.employee_assistant.schemas import FileMetadata
from src.employee_assistant.utils import get_file_size_by_base64, get_file_extension


class DocxImageExtractor(ImageExtractor):
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = file_path if isinstance(file_path, str) else str(file_path)

    def extract(self) -> list[FileMetadata]:
        document = Document(self.file_path)
        files: list[FileMetadata] = []
        id = 0
        for _, rel in document.part.rels.items():
            if "image" in rel.target_ref:
                image_src = rel.target_ref.split("/")[-1]
                image_data = rel.target_part.blob
                image_base64 = base64.b64encode(image_data).decode("utf-8")
                id += 1
                file = FileMetadata(
                    file_path=image_src,
                    format=get_file_extension(image_src),
                    size=get_file_size_by_base64(image_base64),
                    file_base64=image_base64,
                    payload={"image_id": f"image{id}"}
                )
                files.append(file)
        return files
