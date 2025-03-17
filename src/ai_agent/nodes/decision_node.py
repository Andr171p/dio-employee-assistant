from typing import TYPE_CHECKING, Literal, Union

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable
    from langchain_core.language_models import BaseChatModel, LLM

from langgraph.types import Command
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.ai_agents.base_node import BaseNode
from src.ai_agents.states import GraphState
from src.ai_agents.steps import FirstStep
from src.misc.file_readers import read_txt
from src.config import BASE_DIR


SYSTEM_PROMPT = BASE_DIR / "prompts" / "decision_prompt.txt"

NODES = Literal[
    "retrieve",
    "rewrite"
]


class DecisionNode(BaseNode):
    def __init__(self, model: Union["BaseChatModel", "LLM"]) -> None:
        self._model = model

    def _create_chain(self) -> "Runnable":
        parser = PydanticOutputParser(pydantic_object=FirstStep)
        prompt = ChatPromptTemplate.from_messages([
            ("system", read_txt(SYSTEM_PROMPT)),
        ]).partial(format_instructions=parser.get_format_instructions())
        return prompt | self._model | parser

    async def execute(self, state: GraphState) -> Command[NODES]:
        print("---Decision---")
        chain = self._create_chain()
        response = await chain.ainvoke({"question": state.get("question")})
        print(response)
        decision = response.decision
        update = {"question": state.get("question"), "decision": decision}
        return Command(update=update, goto=decision)
