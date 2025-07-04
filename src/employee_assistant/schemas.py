from typing import Optional

from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, field_validator, FilePath, Field, model_validator


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class Grade(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"


class BaseMessage(BaseModel):
    id: int
    role: Role
    chat_id: str | int
    text: str
    grade: Optional[Grade] = None

    @classmethod
    @field_validator("chat_id")
    def validate_chat_id(cls, chat_id: str | int) -> str:
        return str(chat_id)


class FileMetadata(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Уникальный ID файла
    file_path: FilePath                      # Путь к файлу
    file_name: Optional[str] = None          # Имя файла
    format: str                              # Формат файла
    size_mb: float                           # Размер файла в мб
    source: Optional[str] = None             # Источник
    file_base64: Optional[str] = None        # Файл в base64 строке

    @model_validator(mode="after")
    def set_file_name(self) -> "FileMetadata":
        if self.file_name is None:
            self.file_name = self.file_path.name
        return self


class ImageMetadata(FileMetadata):
    image_id: str


class MarkdownDocument(BaseModel):
    source: str
    content: str
    additional_files: list[FileMetadata]


class Chunk(BaseModel):
    text: str
    length: int
    metadata: list[FileMetadata]
