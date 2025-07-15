from typing import Optional, Callable, Sized
from functools import cached_property

import spacy

from pydantic import BaseModel, Field

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

from langchain_text_splitters import (
    TextSplitter,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)

from .templates import (
    TITLE_GENERATION_TEMPLATE,
    SUMMARIZATION_TEMPLATE,
    KEYWORDS_EXTRACTION_TEMPLATE
)

DEFAULT_NER_MODEL = "ru_core_news_md"

ENRICHED_CHUNK = """Название: {title}
Содержание: {content}
Краткое содержание: {summary}
Ключевые слова: {keywords}
"""

ENRICHED_WITH_HEADERS_CHUNK = """Название: {title}
Главный заголовок: {h1}
Подзаголовок: {h2}
Мелкий заголовок: {h3}
Содержание: {content}
Краткое содержание: {summary}
Ключевые слова: {keywords}
"""

HEADERS_TO_SPLIT_ON: list[tuple[str, str]] = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]


def extract_keywords_using_nlp(text: str, nlp: spacy.Language) -> list[str]:
    return [token.text for token in nlp(text) if token.pos_ in ["NOUN", "PROPN"]]


def extract_keywords_using_llm(text: str, llm: BaseChatModel) -> list[str]:
    class KeywordsResponse(BaseModel):
        keywords: list[str] = Field(..., description="Ключевые слова для поиска.")

    parser = PydanticOutputParser(pydantic_object=KeywordsResponse)
    llm_chain = (
            ChatPromptTemplate
            .from_messages([("system", KEYWORDS_EXTRACTION_TEMPLATE)])
            .partial(format_instructions=parser.get_format_instructions())
            | llm
            | parser
    )
    response: KeywordsResponse = llm_chain.invoke({"text": text})
    return response.keywords


class EnrichedMarkdownTextSplitter(TextSplitter):
    """
        Text splitter for Markdown documents with additional chunk enriched.

        This splitter does:
        1. Dividing a Markdown document by headings (h1-h6).
        2. Additional recursive change on cups of the displayed size.
        3. Enriched of each chunk:
            - Header generation.
            - Creating a summary.
            - Keywords extraction (using NLP or LLM)

        Args:
            chunk_size (int): Max size of chunk in characters.
            chunk_overlap (int): Overlap between adjacent chunks in characters.
            length_function: (Callable[[Sized], int]): Function for computing length of text.
            llm: (BaseChatModel): LLM model for title generation, summarization and keyword extraction.
            use_md_headers_splitter: (bool, optional): Using Markdown splitting by headers.
            use_llm_for_ner: (bool, optional): Using LLM for keyword extraction, default False.
            ner_model: (str, optional): NER model for keyword extraction, default None.
    """
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
            length_function: Callable[[Sized], int],
            llm: BaseChatModel,
            use_md_headers_splitter: bool = False,
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
        self._use_md_headers_splitter = use_md_headers_splitter
        self._headers_to_split_on = HEADERS_TO_SPLIT_ON
        self._markdown_splitter = MarkdownHeaderTextSplitter(self._headers_to_split_on)
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )

    @cached_property
    def _nlp(self) -> spacy.Language:
        return spacy.load(self._ner_model)

    def split_text(self, text: str) -> list[str]:
        documents = self._markdown_splitter.split_text(text) if self._use_md_headers_splitter \
            else [Document(page_content=text)]
        title = self._generate_title(text)
        enriched_chunks: list[str] = []
        for document in documents:
            headers = document.metadata
            chunks = self._recursive_splitter.split_text(document.page_content)
            for chunk in chunks:
                enriched_chunk = self._enrich_chunk(title, headers, chunk)
                enriched_chunks.append(enriched_chunk)
        return enriched_chunks

    def _enrich_chunk(
            self,
            title: str,
            headers: Optional[dict[str, str]],
            chunk: str
    ) -> str:
        summary = self._summarize(chunk)
        keywords = self._extract_keywords(chunk)
        keywords = " ".join(keywords)
        if self._use_md_headers_splitter:
            return ENRICHED_WITH_HEADERS_CHUNK.format(
                title=title,
                h1=headers.get("h1"),
                h2=headers.get("h2"),
                h3=headers.get("h3"),
                content=chunk,
                summary=summary,
                keywords=keywords
            )
        return ENRICHED_CHUNK.format(
            title=title,
            content=chunk,
            summary=summary,
            keywords=keywords
        )

    def _generate_title(self, text: str) -> str:

        class TitleResponse(BaseModel):
            title: str = Field(..., description="Заголовок или основная тема текста.")

        parser = PydanticOutputParser(pydantic_object=TitleResponse)
        llm_chain = (
            ChatPromptTemplate
            .from_messages([("system", TITLE_GENERATION_TEMPLATE)])
            .partial(format_instructions=parser.get_format_instructions())
            | self._llm
            | parser
        )
        response: TitleResponse = llm_chain.invoke({"text": text})
        return response.title

    def _summarize(self, text: str) -> str:
        llm_chain = ChatPromptTemplate.from_template(SUMMARIZATION_TEMPLATE) | self._llm | StrOutputParser()
        summary = llm_chain.invoke({"text": text})
        return summary

    def _extract_keywords(self, text: str) -> list[str]:
        keywords = extract_keywords_using_llm(text, llm=self._llm) if self._use_llm_for_ner \
            else extract_keywords_using_nlp(text, nlp=self._nlp)
        return keywords
