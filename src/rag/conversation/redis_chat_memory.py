from typing import List, Dict

from langchain_community.chat_message_histories import RedisChatMessageHistory

from src.rag.conversation.base_chat_memory import BaseChatMemory


class RedisChatMemory(BaseChatMemory):
    def __init__(self, session_id: str, ttl: int = 3600) -> None:
        self._history = RedisChatMessageHistory(
            session_id=session_id,
            ttl=ttl
        )

    def get_messages(self) -> List[Dict]:
        return [message.model_dump() for message in self._history.messages]

    def add_message(self, message: Dict) -> None:
        if message["type"] == "human":
            self._history.add_user_message(message["content"])
        else:
            self._history.add_ai_message(message["content"])

    def clear(self) -> None:
        self._history.clear()
