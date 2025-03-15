from langchain_core.retrievers import BaseRetriever

from src.agent.states import GraphState
from src.agent.utils import format_docs


class RetrieverNode:
    def __init__(self, retriever: BaseRetriever) -> None:
        self._retriever = retriever

    def retrieve(self, state: GraphState) -> dict:
        print("---RETRIEVE---")
        question = state["question"]
        documents = self._retriever.get_relevant_documents(question)
        return {"documents": format_docs(documents), "question": question}

    def __call__(self, state: GraphState) -> dict:
        return self.retrieve(state)
