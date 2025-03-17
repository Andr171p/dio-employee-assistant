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


REASONER_TEMPLATE = BASE_DIR / "prompts" / "Агент_ризонер.txt"


class ReasonerNode(BaseNode):
    def __init__(self, model: Union["BaseChatModel", "LLM"]) -> None:
        self._model = model

    def _build_chain(self) -> "Runnable":
        parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages(
            ("system", read_txt(REASONER_TEMPLATE))
        )
        return prompt | self._model | parser

    async def execute(self, state: ReasoningState) -> dict:
        print("---REASONING---")
        chain = self._build_chain()
        last_reason = await chain.ainvoke({"user_question": state.get("user_question")})
        return {"last_reason": last_reason}
