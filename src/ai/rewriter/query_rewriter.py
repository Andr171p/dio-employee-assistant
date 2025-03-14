from typing import TYPE_CHECKING, Union, Any, Optional

if TYPE_CHECKING:
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel, LLM
    from langchain_core.output_parsers import BaseTransformOutputParser

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output

from src.ai.utils.chain_factories import get_chain


class QueryRewriter(Runnable):
    def __init__(
            self,
            prompt: "BasePromptTemplate",
            model: Union["BaseChatModel", "LLM"],
            parser: "BaseTransformOutputParser",
    ) -> None:
        self._prompt = prompt
        self._model = model
        self._parser = parser

    def invoke(self, query: str, **kwargs: Any) -> str:
        chain = get_chain(
            prompt=self._prompt,
            model=self._model,
            parser=self._parser
        )
        return chain.invoke({"query": query})

    async def ainvoke(
            self,
            input: Input,
            config: Optional[RunnableConfig] = None,
            **kwargs: Any
    ) -> Output:
        chain = get_chain(
            prompt=self._prompt,
            model=self._model,
            parser=self._parser
        )
        return await chain.ainvoke(input, config, **kwargs)
