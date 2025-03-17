from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable
    from langchain_core.language_models import BaseChatModel, LLM

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.ai_agents.base_node import BaseNode
from src.ai_agents.states import GraphState
from src.misc.file_readers import read_txt
from src.config import BASE_DIR


TEMPLATE = BASE_DIR / "prompts" / "critic_prompt.txt"


class CritiqueNode(BaseNode):
    def __init__(self, model: Union["BaseChatModel", "LLM"]) -> None:
        self._model = model

    def _create_chain(self) -> "Runnable":
        parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_template(read_txt(TEMPLATE))
        return prompt | self._model | parser

    async def execute(self, state: GraphState) -> dict:
        ...
