from functools import wraps
from typing import Callable

from src.rag.chat_memory.redis_chat_memory import RedisChatMemory


def save_chat_memory(generate: Callable) -> Callable:
    @wraps(generate)
    async def wrapper(self, query: str, **kwargs) -> str:
        session_id: str = kwargs.get("session_id")
        if not session_id:
            raise ValueError("session_id is required for Redis chat memory")
        response = await generate(self, query, **kwargs)
        memory = RedisChatMemory(session_id)
        memory.add_message({"type": "human", "content": query})
        memory.add_message({"type": "ai", "content": response})
        return response
    return wrapper