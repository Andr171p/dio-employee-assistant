from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from langchain_core.documents import Document

import numpy as np
from sentence_transformers import CrossEncoder
from langchain_core.runnables import RunnableSerializable, RunnableConfig
from langchain_core.runnables.utils import Output

from src.ai.reranker.base_reranker import BaseReranker


class CrossEncoderReranker(RunnableSerializable, BaseReranker):
    def __init__(self, model_name: str, top_n: int = 5, device: str = "cpu") -> None:
        super().__init__()
        self._top_n = top_n
        self._cross_encoder = CrossEncoder(
            model_name=model_name,
            device=device
        )

    def rerank(
            self,
            query: str,
            documents: List["Document"],
            return_scores: bool = False
    ) -> List[Union["Document", None]]:
        if not documents:
            return []
        pairs = [[query, document.page_content] for document in documents]
        scores = self._cross_encoder.predict(pairs)
        sorted_indices = np.argsort(scores)[::-1]
        sorted_documents = [documents[i] for i in sorted_indices]
        if return_scores:
            for document, score in zip(sorted_documents, scores[sorted_indices]):
                document.metadata["score"] = float(score)
        # print(sorted_documents[:self._top_n])
        return sorted_documents[:self._top_n]

    def invoke(
            self,
            input: Dict,
            config: Optional[RunnableConfig] = None,
            **kwargs: Any
    ) -> List["Document"]:
        if "query" not in input or "documents" not in input:
            raise ValueError("Input must contain 'query' and 'documents' keys")
        return self.rerank(
            query=input["question"],
            documents=input["context"]
        )

    async def ainvoke(
            self,
            input: Dict,
            config: Optional[RunnableConfig] = None,
            **kwargs: Any
    ) -> Output:
        print(input)
        print(len(input["context"]))
        return self.rerank(
            query=input["question"],
            documents=input["context"],
        )
