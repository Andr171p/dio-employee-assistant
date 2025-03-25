from typing import Union

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.language_models import BaseChatModel, LLM

from src.config import BASE_DIR
from src.dio_ai_agent.state import State
from src.misc.file_readers import read_txt
from src.dio_ai_agent.nodes.base_node import BaseNode
from src.dio_ai_agent.format_instructions import CurrentChapter


LIBRARIAN_TEMPLATE = BASE_DIR / "prompts" / "dio" / "Библиотекарь.txt"


class LibrarianNode(BaseNode):
    def __init__(self, model: Union[BaseChatModel, LLM]) -> None:
        parser = PydanticOutputParser(pydantic_object=CurrentChapter)
        prompt = ChatPromptTemplate.from_messages([
            ("system", read_txt(LIBRARIAN_TEMPLATE))
        ]).partial(format_instructions=parser.get_format_instructions())
        self._chain = prompt | model | parser

    async def execute(self, state: State) -> dict:
        print("---CHOICE OF CHAPTER---")
        response = await self._chain.ainvoke({"user_question": state["user_question"]})
        chapter = response.chapter
        print(chapter)
        return {"chapter": chapter}
