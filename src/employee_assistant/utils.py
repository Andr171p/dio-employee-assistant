

def get_file_size_by_base64(base64_data: str) -> float:
    """Получает размер файла в мб по его base64 строке."""
    if base64_data.startswith("data:"):
        base64_data = base64_data.split(",", 1)[1]
    padding = base64_data.count("=")
    clean_length = len(base64_data) - padding
    size_bytes = (clean_length * 3) / 4
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)


def get_file_extension(file_path: str) -> str:
    """Получает расширение файла по его имени."""
    return file_path.split(".")[-1]
