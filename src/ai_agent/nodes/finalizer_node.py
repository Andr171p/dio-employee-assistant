from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable
    from langchain_core.language_models import BaseChatModel, LLM

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.ai_agent.states import ReasoningState
from src.ai_agent.nodes.base_node import BaseNode
from src.misc.file_readers import read_txt
from src.config import BASE_DIR


FINALIZER_TEMPLATE = BASE_DIR / "prompts" / "Финализатор.txt"


class FinalizerNode(BaseNode):
    def __init__(self, model: Union["BaseChatModel", "LLM"]) -> None:
        self._model = model

    def _build_chain(self) -> "Runnable":
        parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages(("system", read_txt(FINALIZER_TEMPLATE)))
        return prompt | self._model | parser

    async def execute(self, state: ReasoningState) -> dict:
        print("---FINALIZE---")
        chain = self._build_chain()
        final_answer = await chain.ainvoke(
            {
                "user_question": state.get("user_question"),
                "last_reason": state.get("last_reason"),
                "critique": state.get("critique", ""),
                "last_answer": state.get("last_answer", ""),
                "search_results": state.get("search_results", [])
            }
        )
        return {"final_answer": final_answer}
