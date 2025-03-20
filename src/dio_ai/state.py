from typing_extensions import TypedDict


class GraphState(TypedDict):
    user_question: str
    chapter: str
    context: str
    final_answer: str
