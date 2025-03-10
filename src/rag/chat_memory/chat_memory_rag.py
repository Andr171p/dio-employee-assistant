from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts import BasePromptTemplate
    from langchain_core.language_models import BaseChatModel
    from langchain_core.output_parsers import BaseTransformOutputParser
    from langchain.memory.chat_memory import BaseChatMemory

from langchain_core.runnables import RunnablePassthrough

from src.rag.base_rag import BaseRAG
from src.rag.rag_utils import format_docs


class ChatMemoryRAG(BaseRAG):
    def __init__(
            self,
            retriever: "BaseRetriever",
            prompt: "BasePromptTemplate",
            model: "BaseChatModel",
            parser: "BaseTransformOutputParser",
            memory: "BaseChatMemory",
    ) -> None:
        self._retriever = retriever
        self._memory = memory
        self._prompt = prompt
        self._model = model
        self._parser = parser
        self._chain = (
                {
                    "context": self._retriever | format_docs,
                    "question": RunnablePassthrough(),
                    "history": lambda x: self._memory.load_memory_variables(x)["history"],
                } |
                self._prompt |
                self._model |
                self._parser
        )

    async def generate(self, query: str, **kwargs) -> str:
        result =  await self._chain.invoke(query)
        self._memory.save_context(
            inputs={"input": query},
            outputs={"output": result}
        )
        return result
