'''import logging
import asyncio

from aiogram import Bot

from src.employee_assistant.container import container
from src.employee_assistant.bot.commands import set_commands
from src.employee_assistant.bot.dispatcher import create_dispatcher


async def main() -> None:
    bot = await container.get(Bot)
    dp = create_dispatcher()
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())'''

import re

from docx2md import DocxFile, DocxMedia, Converter

file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Инструкции\ИНСТРУКЦИЯ_по_заполнению_в_1С_УФФ_документа_Задание_сотруднику_29.docx"


def do_convert(docx_file: str, target_dir: str = "", use_md_table: bool = True) -> str:
    try:
        docx = DocxFile(docx_file)
        media = DocxMedia(docx)
        if target_dir:
            media.save(target_dir)
        converter = Converter(docx.document(), media, use_md_table)
        return converter.convert()
    except Exception as e:
        return f"Exception: {e}"


def extract_image_ids(md_text: str) -> list[str]:
    pattern = r'<img\s+[^>]*id="([^"]+)"'  # Ищет id в тегах <img>
    return re.findall(pattern, md_text)


text = do_convert(file_path)
print(text)
print(extract_image_ids(text))
