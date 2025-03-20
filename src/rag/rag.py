from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel, LLM
    from langchain_core.output_parsers import BaseTransformOutputParser

from langchain_core.runnables import RunnablePassthrough

from src.rag.base_rag import BaseRAG
from src.utils.documents import format_docs


class RAG(BaseRAG):
    def __init__(
            self,
            retriever: "BaseRetriever",
            prompt: "BasePromptTemplate",
            model: Union["BaseChatModel", "LLM"],
            parser: "BaseTransformOutputParser",
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
