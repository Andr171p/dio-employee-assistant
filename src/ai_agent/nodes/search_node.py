from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever

from src.ai_agent.nodes.base_node import BaseNode
from src.ai_agent.states import ReasoningState
from src.ai_agent.utils import format_docs


class SearchNode(BaseNode):
    def __init__(self, retriever: "BaseRetriever") -> None:
        self._retriever = retriever

    async def execute(self, state: ReasoningState) -> dict:
        print("---RETRIEVE---")
        documents = await self._retriever.ainvoke(state.get("user_question", ""))
        search_results = format_docs(documents)
        return {"search_results": search_results}
