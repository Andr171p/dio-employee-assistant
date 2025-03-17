from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever

from src.ai_agent.nodes.base_node import BaseNode
from src.ai_agent.states import GraphState
from src.ai_agent.utils import format_docs


class RetrieverNode(BaseNode):
    def __init__(self, retriever: "BaseRetriever") -> None:
        self._retriever = retriever

    async def execute(self, state: GraphState) -> dict:
        print("---RETRIEVE---")
        documents = await self._retriever.ainvoke(state.get("user_question"))
        documents = format_docs(documents)
        return {"context": context}
