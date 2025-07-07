from typing_extensions import TypedDict

from pathlib import Path

from langchain_core.document_loaders import BaseLoader


class ImageMetadata(TypedDict):
    src: str            # Path to image in document
    source: str | Path  # Source file
    format: str         # Image format (png, jpg, ...)
    size_mb: float      # File size in MB
    str_base64: str     # base64 string with images


def get_size_by_base64(str_base64: str) -> float:
    """Receive file size in MB by base64 string."""
    if str_base64.startswith("data:"):
        str_base64 = str_base64.split(",", 1)[1]
    padding = str_base64.count("=")
    clean_length = len(str_base64) - padding
    size_bytes = (clean_length * 3) / 4
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)


class Base2MdLoader(BaseLoader):
    @property
    def file_name(self) -> str:
        raise NotImplementedError

    @property
    def file_type(self) -> str:
        raise NotImplementedError

    def _load_images(self) -> list[ImageMetadata]:
        """Method for loading images in base64 from document."""
        raise NotImplementedError
