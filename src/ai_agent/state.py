from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

from langgraph.graph.message import add_messages


class State(TypedDict):
    user_question: str
    chapter: str
    final_answer: str


class StateWithMessages(TypedDict):
    messages: List[str]
    chapter: str
    final_answer: str
