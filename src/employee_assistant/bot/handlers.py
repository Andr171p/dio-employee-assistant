from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from dishka.integrations.aiogram import FromDishka as Depends

from .decorators import messages_saver
from .keyboards import grade_kb, GradeCallback

from ..base import AIAgent, MessageRepository

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("...")


@router.message(F.text)
@messages_saver
async def answer(message: Message, ai_agent: Depends[AIAgent]) -> Message:
    await message.bot.send_chat_action(message.chat.id, "typing")
    text = await ai_agent.generate(thread_id=message.from_user.id, content=message.text)
    return await message.answer(text=text, reply_markup=grade_kb(message_id=message.message_id))


@router.callback_query(GradeCallback.filter())
async def rate_message(
        call: CallbackQuery,
        callback_data: GradeCallback,
        message_repository: Depends[MessageRepository]
) -> None:
    await call.answer()
    await message_repository.update(callback_data.message_id, grade=callback_data.grade)
    await call.answer("Оценка поставлена!", show_alert=True)
