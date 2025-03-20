from typing import Union

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.language_models import BaseChatModel, LLM

from src.ai_agent.nodes.base_node import BaseNode
from src.ai_agent.states import ReasoningState
from src.ai_agent.format_instructions import LetterCritique
from src.misc.file_readers import read_txt
from src.config import BASE_DIR


LETTER_EXPERT_SYSTEM_MESSAGE = BASE_DIR / "prompts" / "Эксперт_деловых_писем_ДИО.txt"


class RewriterNode(BaseNode):
    def __init__(self, model: Union[BaseChatModel, LLM]) -> None:
        parser = PydanticOutputParser(pydantic_object=LetterCritique)
        prompt = ChatPromptTemplate.from_messages([
            ("system", read_txt(LETTER_EXPERT_SYSTEM_MESSAGE))
        ]).partial(format_instructions=parser.get_format_instructions())
        self._chain = prompt | model | parser

    async def execute(self, state: ReasoningState) -> dict:
        response = await self._chain.ainvoke({"user_letter": state["user_letter"]})
        critique = response.critique
        rewritten_letter = response.rewritten_letter
        return {"critique": critique, "rewritten_letter": rewritten_letter}
