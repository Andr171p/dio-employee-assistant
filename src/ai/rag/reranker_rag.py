from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

    from src.ai.reranker import CrossEncoderReranker

from src.ai.rag.base_rag import BaseRAG
from src.ai.utils.chain_factories import get_reranker_rag_chain


class RerankerRAG(BaseRAG):
    def __init__(
            self,
            retriever: "BaseRetriever",
            reranker: "CrossEncoderReranker",
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser",
    ) -> None:
        self._retriever = retriever
        self._reranker = reranker
        self._prompt = prompt
        self._model = model
        self._parser = parser

    async def generate(self, query: str, **kwargs) -> str:
        rag_chain = get_reranker_rag_chain(
            retriever=self._retriever,
            reranker=self._reranker,
            prompt=self._prompt,
            model=self._model,
            parser=self._parser
        )
        return await rag_chain.ainvoke(query)
