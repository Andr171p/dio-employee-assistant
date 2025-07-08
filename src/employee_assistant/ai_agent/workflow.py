from typing import Union

from uuid import UUID

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from langchain_core.runnables.config import RunnableConfig

from .states import RAGState
from .nodes import SummarizeNode, RetrieveNode, GenerateNode, MultimodalGenerateNode

IdType = Union[str, int, UUID]


def build_rag(
        summarize: SummarizeNode,
        retrieve: RetrieveNode,
        generate: GenerateNode | MultimodalGenerateNode,
        checkpointer: BaseCheckpointSaver
) -> CompiledStateGraph:
    workflow = StateGraph(RAGState)

    workflow.add_node("summarize", summarize)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    workflow.add_edge(START, "summarize")
    workflow.add_edge("summarize", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile(checkpointer=checkpointer)


async def chat(thread_id: IdType, content: str, agent: CompiledStateGraph) -> str:
    config = RunnableConfig()
    config["configurable"] = {"thread_id": str(thread_id)}
    inputs = {"messages": [{"role": "human", "content": content}]}
    outputs = await agent.ainvoke(inputs, config=config)
    return outputs["messages"][-1]
