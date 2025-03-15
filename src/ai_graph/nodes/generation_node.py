from langchain_core.prompts import BasePromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseTransformOutputParser

from src.ai_graph.states import GraphState


class GenerationNode:
    def __init__(
            self,
            prompt: BasePromptTemplate,
            model: BaseChatModel,
            parser: BaseTransformOutputParser
    ) -> None:
        self._chain = prompt | model | parser

    def generate(self, state: GraphState) -> dict:
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]
        generation = self._chain.invoke({"context": documents, "question": question})
        return {
            "documents": documents,
            "generation": generation,
            "question": question
        }
