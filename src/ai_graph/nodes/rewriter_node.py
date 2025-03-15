from langchain_core.prompts import BasePromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseTransformOutputParser

from src.ai_graph.states import GraphState


class RewriterNode:
    def __init__(
            self,
            prompt: BasePromptTemplate,
            model: BaseChatModel,
            parser: BaseTransformOutputParser,
    ) -> None:
        self._chain = prompt | model | parser

    def rewrite(self, state: GraphState) -> dict:
        print("---REWRITE QUESTION---")
        question = state["question"]
        documents = state["documents"]
        rewritten_question = self._chain.invoke({"question": question})
        return {"documents": documents, "question": rewritten_question}
