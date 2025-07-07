from typing import Optional, Callable

from functools import cached_property

import spacy

from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

from langchain_text_splitters import (
    TextSplitter,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)

DEFAULT_NER_MODEL = ""

ENRICHED_CHUNK_TEMPLATE = """Название: {title}
Содержание: {text}
Краткое содержание: {summary}
Ключевые слова: {keywords}
"""


def extract_keywords_using_nlp(text: str, nlp: spacy.Language) -> list[str]:
    return [token.text for token in nlp(text) if token.pos_ in ["NOUN", "PROPN"]]


def extract_keywords_using_llm(text: str, llm: BaseChatModel) -> list[str]:
    class KeywordsResponse(BaseModel):
        keywords: list[str] = Field(..., description="Ключевые слова для поиска.")

    parser = PydanticOutputParser(pydantic_object=KeywordsResponse)
    llm_chain = (
            ChatPromptTemplate
            .from_messages([SystemMessage(...)])
            .partial(format_instructions=parser.get_format_instructions())
            | llm
            | parser
    )
    response: KeywordsResponse = llm_chain.invoke({"text": text})
    return response.keywords


class EnrichedMarkdownTextSplitter(TextSplitter):
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
            length_function: Callable[..., int],
            header_to_split_on: list[tuple[str, str]],
            llm: BaseChatModel,
            use_llm_for_ner: bool = False,
            ner_model: Optional[str] = None
    ) -> None:
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )
        self._llm = llm
        self._use_llm_for_ner = use_llm_for_ner
        self._ner_model = ner_model if ner_model else DEFAULT_NER_MODEL
        self._markdown_splitter = MarkdownHeaderTextSplitter(header_to_split_on)
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            length_function=self._length_function
        )

    @cached_property
    def _nlp(self) -> spacy.Language:
        return spacy.load(self._ner_model)

    def split_text(self, text: str) -> list[str]:
        documents = self._markdown_splitter.split_text(text)
        title = self.__generate_title(text)
        enriched_texts: list[str] = []
        for document in documents:
            texts = self._recursive_splitter.split_text(document.page_content)
            for text in texts:
                enriched_text = self.__enrich(title, text)
                enriched_texts.append(enriched_text)
        return enriched_texts

    def __enrich(self, title: str, text: str) -> str:
        summary = self.__summarize(text)
        keywords = self.__extract_keywords(text)
        return ENRICHED_CHUNK_TEMPLATE.format(
            title=title, text=text, summary=summary, keywords=keywords
        )

    def __generate_title(self, text: str) -> str:

        class TitleResponse(BaseModel):
            title: str = Field(..., description="Заголовок или основная тема текста.")

        parser = PydanticOutputParser(pydantic_object=TitleResponse)
        llm_chain = (
            ChatPromptTemplate
            .from_messages([SystemMessage(...)])
            .partial(format_instructions=parser.get_format_instructions())
            | self._llm
            | parser
        )
        response: TitleResponse = llm_chain.invoke({"text": text})
        return response.title

    def __summarize(self, text: str) -> str:
        llm_chain = ChatPromptTemplate.from_template(...) | self._llm | StrOutputParser()
        summary = llm_chain.invoke({"text": text})
        return summary

    def __extract_keywords(self, text: str) -> list[str]:
        keywords = extract_keywords_using_llm(text, llm=self._llm) if self._use_llm_for_ner \
            else extract_keywords_using_nlp(text, nlp=self._nlp)
        return keywords
