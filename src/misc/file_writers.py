import aiofiles
from pathlib import Path
from typing import BinaryIO, Union


async def write_eml(
        file_path: Union[Path, str],
        binary_file: BinaryIO,
) -> None:
    async with aiofiles.open(
        file=file_path,
        mode="wb"
    ) as file:
        await file.write(binary_file.read())
