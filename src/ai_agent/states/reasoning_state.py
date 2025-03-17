from typing import List
from typing_extensions import TypedDict


class ReasoningState(TypedDict):
    last_reason: str
    user_question: str
    last_answer: str
    critique: List[str]
    final_decision: str
    final_answer: str
    search_query: str
    context: str
