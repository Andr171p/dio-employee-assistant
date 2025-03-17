import os
import uuid
from pathlib import Path
from typing import BinaryIO, Union


def write_eml(
        binary_file: BinaryIO,
        directory: Union[Path, str]
) -> None:
    with open(
        file=os.path.join(directory, f"{uuid.uuid4()}.eml"),
        mode="wb"
    ) as file:
        file.write(binary_file.read())
