from langchain_core.prompts import BasePromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseTransformOutputParser

from src.agent.states import GraphState


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
        print("GENERATED:", generation)
        return {"documents": documents, "generation": generation, "question": question}

    def __call__(self, state: GraphState) -> dict:
        return self.generate(state)
