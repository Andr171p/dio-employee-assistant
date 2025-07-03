from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables.config import RunnableConfig

from .states import RAGState
from .nodes import SummarizeNode, RetrieveNode, GenerateNode

from ..base import AIAgent


def create_rag_workflow(
        summarize: SummarizeNode,
        retrieve: RetrieveNode,
        generate: GenerateNode,
        checkpointer: ...
) -> CompiledStateGraph:
    workflow = (
        StateGraph(RAGState)
        .add_node("summarize", summarize)
        .add_node("retrieve", retrieve)
        .add_node("generate", generate)
        .add_edge(START, "summarize")
        .add_edge("summarize", "retrieve")
        .add_edge("retrieve", "generate")
        .add_edge("generate", END)
    )
    return workflow.compile(checkpointer=checkpointer)


class RAGAgent(AIAgent):
    def __init__(
            self,
            retriever: BaseRetriever,
            model: BaseChatModel,
            checkpointer: BaseCheckpointSaver
    ) -> None:
        self.graph = create_rag_workflow(
            summarize=SummarizeNode(model),
            retrieve=RetrieveNode(retriever),
            generate=GenerateNode(model),
            checkpointer=checkpointer
        )

    async def generate(self, thread_id: str | int, content: str) -> str:
        config = RunnableConfig()
        config["configurable"] = {"thread_id": str(thread_id)}
        # config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": content}]}
        outputs = await self.graph.ainvoke(inputs, config=config)
        return outputs["messages"][-1]
