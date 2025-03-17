from typing import TYPE_CHECKING, Union, Literal

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable
    from langchain_core.language_models import BaseChatModel, LLM

from langgraph.types import Command
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.ai_agent.nodes.base_node import BaseNode
from src.ai_agent.states import ReasoningState
from src.ai_agent.instructions import Critique
from src.misc.file_readers import read_txt
from src.config import BASE_DIR


SYSTEM_MESSAGE = BASE_DIR / "prompts" / "Критик.txt"

ACTIONS = Literal[
    "finalize",
    "search",
    "critique"
]


class CritiqueNode(BaseNode):
    def __init__(self, model: Union["BaseChatModel", "LLM"]) -> None:
        self._model = model

    def _build_chain(self) -> "Runnable":
        parser = PydanticOutputParser(pydantic_object=Critique)
        prompt = ChatPromptTemplate.from_messages([
            ("system", read_txt(SYSTEM_MESSAGE))
        ]).partial(format_instructions=parser.get_format_instructions())
        return prompt | self._model | parser.parser

    async def execute(self, state: ReasoningState) -> Command[ACTIONS]:
        print("---CRITIQUE NODE EXECUTE---")
        chain = self._build_chain()
        response = await chain.ainvoke(
            {
                "user_question": state.get("user_question"),
                "last_reason": state.get("last_reason"),
                "last_answer": state.get("last_answer", ""),
                "old_critique": state.get("critique", []),
                "search_results": state.get("search_results", ""),
            }
        )
        final_decision = response.final_decision
        critique = response.critique
        search_query = response.search_query
        new_critique = state.get("critique", [])
        if new_critique is None:
            new_critique = []
        new_critique = new_critique.append(critique)
        update = {
            "final_decision": final_decision,
            "critique": new_critique,
            "search_query": search_query
        }
        goto = "finalize"
        if final_decision == "search" and search_query is not None and len(search_query) > 0:
            goto = "search"
        return Command(update=update, goto=goto)
