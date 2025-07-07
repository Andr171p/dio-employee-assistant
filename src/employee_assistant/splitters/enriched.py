from typing import Optional

from abc import ABC, abstractmethod

import spacy

from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import (
    TextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter
)

DEFAULT_NER_MODEL = ""


class BaseKeywordExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> list[str]: pass


class NerKeywordExtractor(BaseKeywordExtractor):
    def __init__(self, nlp: spacy.Language) -> None:
        self.nlp = nlp

    def extract(self, text: str) -> list[str]:
        document = self.nlp(text)
        keywords = [token.text for token in document if token.pos_ in ["NOUN", "PROPN"]]
        return keywords


class LLMKeywordExtractor(BaseKeywordExtractor):
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm

    def extract(self, text: str) -> list[str]:
        ...


class EnrichedMarkdownTextSplitter(TextSplitter):
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
            header_to_split_on: list[tuple[str, str]],
            llm: BaseChatModel,
            use_llm_for_ner: bool = False,
            ner_model: Optional[str] = None
    ) -> None:
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.llm = llm
        self.use_llm_for_ner = use_llm_for_ner
        self.ner_model = ner_model if ner_model else DEFAULT_NER_MODEL
        self.nlp = spacy.load(self.ner_model)
        self.markdown_splitter = MarkdownHeaderTextSplitter(header_to_split_on)
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            length_function=len
        )

    def split_text(self, text: str) -> list[str]:
        pass

    def __enrich(self, text: str) -> str:
        ...

    def __summarize(self, text: str) -> str:
        llm_chain = PromptTemplate.from_template(...) | self.llm | StrOutputParser()
        ...

    def __extract_keyword(self, text: str) -> list[str]:
        keyword_extractor = LLMKeywordExtractor(self.llm) if self.use_llm_for_ner \
            else NerKeywordExtractor(self.nlp)
        keywords = keyword_extractor.extract(text)
        return keywords
