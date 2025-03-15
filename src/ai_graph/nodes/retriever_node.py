from langchain_core.retrievers import BaseRetriever

from src.ai_graph.states import GraphState


class RetrieverNode:
    def __init__(self, retriever: BaseRetriever) -> None:
        self._retriever = retriever

    def retrieve(self, state: GraphState) -> dict:
        print("---RETRIEVE---")
        question = state["question"]
        documents = self._retriever.get_relevant_documents(question)
        return {"documents": documents, "question": question}
