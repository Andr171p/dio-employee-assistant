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

from src.employee_assistant.document_loaders.pdf2markdown import Pdf2MarkdownLoader

file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Инструкции\Инструкция по системе Тикеты.pdf"

loader = Pdf2MarkdownLoader(pdf_path=file_path, include_images=True)

docs = loader.load()

print(docs[0].page_content)