from typing import Callable, Coroutine, Any, TypeVar
from typing_extensions import ParamSpec
from functools import wraps

from aiogram.types import Message

from dishka import Scope

from ..container import container
from ..base import MessageRepository
from ..schemas import BaseMessage, Role

P = ParamSpec("P")                                    # Параметры оригинальной функции
R = TypeVar("R")                                      # Возвращаемый тип оригинальной функции
MessageHandler = Callable[P, Coroutine[Any, Any, R]]  # Обработчик сообщения пользователя


def messages_saver(handler: MessageHandler[P, R]) -> MessageHandler[P, R | None]:
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs) -> R | None:
        async with container(scope=Scope.REQUEST) as request_container:
            message_repository = await request_container.get(MessageRepository)
            user_message = BaseMessage(
                id=message.message_id,
                role=Role.USER,
                chat_id=message.from_user.id,
                text=message.text
            )
            msg = await handler(message, *args, **kwargs)
            assistant_message = BaseMessage(
                id=msg.message_id,
                role=Role.ASSISTANT,
                chat_id=message.from_user.id,
                text=msg.text
            )
            await message_repository.bulk_create([user_message, assistant_message])
        return handler
    return wrapper
