from typing import Optional, Callable

import spacy

from pydantic import BaseModel, Field

from langchain_core.language_models import BaseChatModel

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .ai_agent.utils import create_structured_output_llm_chain, create_llm_chain
from .constants import NER_MODEL_NAME
from .templates import (
    TITLE_EXTRACTION_TEMPLATE,
    CHUNK_SUMMARIZATION_TEMPLATE,
    KEYWORDS_EXTRACTION_TEMPLATE,
    ENRICHED_CHUNK_TEMPLATE,
)


class ExtractedTitle(BaseModel):
    title: str = Field(..., description="Заголовок или основная тема текста.")


class ExtractedKeywords(BaseModel):
    keywords: list[str] = Field(..., description="Ключевые слова для поиска.")


class EnrichedTextSplitter:
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
            length_function: Callable[..., int],
            llm: BaseChatModel,
            ner_model_name: Optional[str] = None,
            use_llm_for_ner: bool = False,
    ) -> None:
        self._llm = llm
        self._ner_model_name = ner_model_name if ner_model_name else NER_MODEL_NAME
        self._nlp = spacy.load(self._ner_model_name)
        self._use_llm_for_ner = use_llm_for_ner
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )

    async def _get_title(self, text: str) -> str:
        """Получает заголовок текста / основную тему текста."""
        llm_chain = create_structured_output_llm_chain(
            output_schema=ExtractedTitle,
            template=TITLE_EXTRACTION_TEMPLATE,
            model=self._llm
        )
        response: ExtractedTitle = await llm_chain.ainvoke({"text": text})
        return response.title

    async def _summarize_chunk(self, chunk: str) -> str:
        """Создаёт краткое содержание чанка."""
        llm_chain = create_llm_chain(CHUNK_SUMMARIZATION_TEMPLATE, self._llm)
        summary = await llm_chain.ainvoke({"text": chunk})
        return summary

    async def _extract_keywords(self, chunk: str) -> list[str]:
        """Извлекает ключевые слова из чанка."""
        if self._use_llm_for_ner:
            return await self.__extract_keywords_with_llm(chunk)
        return self.__extract_keywords_with_nlp(chunk)

    def __extract_keywords_with_nlp(self, chunk: str) -> list[str]:
        """Извлекает ключевые слова из чанка используя NLP модель."""
        document = self._nlp(chunk)
        keywords = [token.text for token in document if token.pos_ in ["NOUN", "PROPN"]]
        return keywords

    async def __extract_keywords_with_llm(self, chunk: str) -> list[str]:
        """Извлекает ключевые слова из чанка используя LLM."""
        llm_chain = create_structured_output_llm_chain(
            output_schema=ExtractedKeywords,
            template=KEYWORDS_EXTRACTION_TEMPLATE,
            model=self._llm
        )
        response: ExtractedKeywords = await llm_chain.ainvoke({"text": chunk})
        return response.keywords

    async def _enrich_chunk(self, chunk: str, title: str, page: Optional[int] = None) -> str:
        """Обогащает чанк метаданными."""
        summary = await self._summarize_chunk(chunk)
        keywords = await self._extract_keywords(chunk)
        return ENRICHED_CHUNK_TEMPLATE.format(
            title=title or "Без названия",
            content=chunk,
            summary=summary,
            keywords="; ".join(keywords) if keywords else "Нет ключевых слов",
            page=page or 0
        )

    async def split_text(self, text: str) -> list[str]:
        """
            Разбивает текст на обогащённые чанки.

            :param text: Исходный текст для обработки
            :return: Список обогащённых чанков
        """
        title = await self._get_title(text)
        chunks = self._splitter.split_text(text)
        enriched_chunks = [
            await self._enrich_chunk(chunk, title=title, page=page)
            for page, chunk in enumerate(chunks)
        ]
        return enriched_chunks
