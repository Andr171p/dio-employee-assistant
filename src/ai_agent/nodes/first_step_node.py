from typing import TYPE_CHECKING, Union, Literal

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable
    from langchain_core.language_models import BaseChatModel, LLM

from langgraph.types import Command
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from src.ai_agent.states import ReasoningState
from src.ai_agent.instructions import FirstStep
from src.ai_agent.nodes.base_node import BaseNode
from src.misc.file_readers import read_txt
from src.config import BASE_DIR


FIRST_STEP_TEMPLATE = BASE_DIR / "prompts" / "Первый_шаг.txt"

ACTIONS = Literal[
    "finalize",
    "search",
    "write"
]


class FirstStepNode(BaseNode):
    def __init__(self, model: Union["BaseChatModel", "LLM"]) -> None:
        self._model = model

    def _build_chain(self) -> "Runnable":
        parser = PydanticOutputParser(pydantic_object=FirstStep)
        prompts = ChatPromptTemplate.from_messages(
            ("system", read_txt(FIRST_STEP_TEMPLATE))
        ).partial(format_instructions=parser.get_format_instructions())
        return prompts | self._model | parser

    async def execute(self, state: ReasoningState) -> Command[ACTIONS]:
        print("---FIRST STEP---")
        chain = self._build_chain()
        response = await chain.ainvoke(
            {
                "user_question": state.get("user_question"),
                "last_reason": state.get("last_reason")
            }
        )
        final_decision = response.final_decision
        search_query = response.search_query
        update = {"final_decision": final_decision, "search_query": search_query}
        goto = "finalize"
        if final_decision == "search" and search_query is not None and len(search_query) > 0:
            goto = "search"
        if final_decision == "writer":
            goto = "write"
        return Command(update=update, goto=goto)
