from typing import List, Dict, Union

from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage


class ChatMessageFactory:
    def __init__(self, chat_history: List[Dict[str, str]]) -> None:
        self._chat_history = chat_history

    def create_chat_message(self) -> ...:
         ...
