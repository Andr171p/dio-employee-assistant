from typing import List
from typing_extensions import TypedDict


class State(TypedDict):
    user_question: str
    chapter: str
    final_answer: str


class StateWithMessages(TypedDict):
    messages: List[str]
    chapter: str
    final_answer: str
