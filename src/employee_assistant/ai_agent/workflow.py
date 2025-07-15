from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from .states import GraphState
from .nodes import (
    SummarizeNode,
    RetrieveNode,
    GenerateNode,
    GenerateWithFilesNode
)


def build_graph(
        summarize_node: SummarizeNode,
        retrieve_node: RetrieveNode,
        generate_node: GenerateNode | GenerateWithFilesNode,
        checkpointer: BaseCheckpointSaver[GraphState]
) -> CompiledStateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node("summarize", summarize_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)

    workflow.add_edge(START, "summarize")
    workflow.add_edge("summarize", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile(checkpointer=checkpointer)
