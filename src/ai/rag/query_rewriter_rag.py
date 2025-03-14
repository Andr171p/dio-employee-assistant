from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser

from src.ai.rag.base_rag import BaseRAG
from src.ai.rewriter import QueryRewriter
from src.ai.utils.chain_factories import get_query_rewriter_rag_chain


class QueryRewriterRAG(BaseRAG):
    def __init__(
            self,
            rewriter: QueryRewriter,
            retriever: "BaseRetriever",
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser",
    ) -> None:
        self._rewriter = rewriter
        self._retriever = retriever
        self._prompt = prompt
        self._model = model
        self._parser = parser

    async def generate(self, query: str, **kwargs) -> str:
        rag_chain = get_query_rewriter_rag_chain(
            rewriter=self._rewriter,
            retriever=self._retriever,
            prompt=self._prompt,
            model=self._model,
            parser=self._parser
        )
        return await rag_chain.ainvoke(query)
