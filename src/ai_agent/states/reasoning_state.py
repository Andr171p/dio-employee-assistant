from typing_extensions import TypedDict


class ReasoningState(TypedDict):
    user_letter: str
    critique: str
    rewritten_letter: str
