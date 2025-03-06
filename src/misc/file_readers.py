from typing import Union

from pathlib import Path


def read_txt(file_path: Union[str, Path]) -> str:
    with open(
            file=file_path,
            mode="r",
            encoding="utf-8"
    ) as file:
        return file.read()
