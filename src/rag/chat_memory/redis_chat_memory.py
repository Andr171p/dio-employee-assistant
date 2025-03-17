from typing import Any, Dict, List, Optional

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output
from langchain_community.chat_message_histories import RedisChatMessageHistory


class RedisChatMemory(Runnable):
    def __init__(self, session_id: str, ttl: int = 3600) -> None:
        self._history = RedisChatMessageHistory(
            session_id=session_id,
            ttl=ttl
        )

    def invoke(self, **kwargs: Any) -> List[Dict]:
        return self.get_messages()

    async def ainvoke(
            self,
            input: Input,
            config: Optional[RunnableConfig] = None,
            **kwargs: Any
    ) -> Output:
        return self.get_messages()

    def get_messages(self) -> List[Dict]:
        return [message.model_dump() for message in self._history.messages]

    def add_message(self, message: Dict) -> None:
        if message["type"] == "human":
            self._history.add_user_message(message["content"])
        else:
            self._history.add_ai_message(message["content"])

    def clear(self) -> None:
        self._history.clear()
