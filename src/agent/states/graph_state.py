from typing import List, Optional
from typing_extensions import TypedDict


class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    generation_quality: Optional[bool]
