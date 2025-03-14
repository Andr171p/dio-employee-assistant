from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from langchain_core.documents import Document

from abc import ABC, abstractmethod


class BaseReranker(ABC):
    @abstractmethod
    def rerank(
        self,
        query: str,
        documents: List["Document"],
        return_scores: bool = False
    ) -> List["Document"]:
        raise NotImplementedError
