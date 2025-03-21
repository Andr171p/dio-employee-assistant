from langgraph.graph import START, StateGraph, END

from src.core.base import BaseAIAssistant
from src.dio_ai.state import GraphState
from src.dio_ai.nodes import LibrarianNode, RAGNode


class Agent(BaseAIAssistant):
    def __init__(self, librarian_node: LibrarianNode, rag_node: RAGNode) -> None:
        graph = StateGraph(GraphState)

        graph.add_node("librarian", librarian_node)
        graph.add_node("rag", rag_node)

        graph.add_edge(START, "librarian")
        graph.add_edge("librarian", "rag")
        graph.add_edge("rag", END)

        self._graph_compiled = graph.compile()

    async def generate(self, user_question: str) -> str:
        response = await self._graph_compiled.ainvoke({"user_question": user_question})
        return response["final_answer"]
