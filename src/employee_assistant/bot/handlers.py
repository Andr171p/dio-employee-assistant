from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from dishka.integrations.aiogram import FromDishka as Depends

from langgraph.graph.state import CompiledGraph

from sqlalchemy.ext.asyncio import AsyncSession

from .decorators import save_messages
from .keyboards import grade_kb, GradeCallback

from ..ai_agent.utils import chat
from ..database.queries import update_message

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("...")


@router.message(F.text)
@save_messages
async def answer(message: Message, agent: Depends[CompiledGraph]) -> Message:
    await message.bot.send_chat_action(message.chat.id, "typing")
    text = await chat(thread_id=message.from_user.id, content=message.text, agent=agent)
    return await message.answer(text=text, reply_markup=grade_kb(message_id=message.message_id))


@router.callback_query(GradeCallback.filter())
async def rate_message(
        call: CallbackQuery,
        callback_data: GradeCallback,
        session: Depends[AsyncSession]
) -> None:
    await update_message(session, callback_data.message_id, grade=callback_data.grade)
    await call.answer("Оценка поставлена!", show_alert=True)
