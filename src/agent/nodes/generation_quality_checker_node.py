from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

from src.agent.states import GraphState


class GenerationQualityCheckerNode:
    def __init__(
            self,
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser"
    ) -> None:
        self._chain = prompt | model | parser

    @staticmethod
    def _get_generation_quality(text: str) -> bool:
        if "Yes" in text:
            return True
        elif "No" in text:
            return False

    def check_generation_quality(self, state: GraphState) -> dict:
        print("---CHECK GENERATION QUALITY---")
        question = state["question"]
        generation = state["generation"]
        documents = state["documents"]
        response = self._chain.invoke({"question": question, "generation": generation})
        print("Generation Quality:", response)
        generation_quality = self._get_generation_quality(response)
        return {
            "question": question,
            "generation": generation,
            "document": documents,
            "generation_quality": generation_quality
        }

    def __call__(self, state: GraphState) -> dict:
        return self.check_generation_quality(state)
