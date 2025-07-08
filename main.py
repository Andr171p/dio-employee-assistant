'''import logging
import asyncio

from aiogram import Bot

from src.employee_assistant.dependencies import container
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


import asyncio

from uuid import uuid4

from langgraph.graph.state import CompiledGraph

from src.employee_assistant.dependencies import container
from src.employee_assistant.ai_agent.utils import chat


async def main() -> None:
    thread_id = str(uuid4())
    question = "На какую кнопку нужно нажать чтобы создать задание и где она находится?"

    agent = await container.get(CompiledGraph)

    text = await chat(thread_id=thread_id, content=question, agent=agent)

    print(text)


asyncio.run(main())
