from typing import Union

from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import BasePromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.language_models import BaseChatModel, LLM
from langchain_core.output_parsers import BaseTransformOutputParser

from src.core.base import BaseAIAssistant
from src.utils.documents import format_docs


class RAG(BaseAIAssistant):
    def __init__(
            self,
            retriever: BaseRetriever,
            prompt: BasePromptTemplate,
            model: Union[BaseChatModel, LLM],
            parser: BaseTransformOutputParser,
    ) -> None:
        self._chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            } |
            prompt |
            model |
            parser
        )

    async def generate(self, query: str, **kwargs) -> str:
        return await self._chain.ainvoke(query)
