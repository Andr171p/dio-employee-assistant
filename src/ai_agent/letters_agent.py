from langgraph.graph import START, StateGraph, END

from src.ai_agent.states import ReasoningState
from src.ai_agent.base_agent import BaseAgent
from src.ai_agent.nodes import RewriterNode


class LettersAgent(BaseAgent):
    def __init__(
            self,
            rewriter_node: RewriterNode
    ) -> None:
        graph = StateGraph(ReasoningState)

        graph.add_node("rewriter", rewriter_node)

        graph.add_edge(START, "rewriter")
        graph.add_edge("rewriter", END)

        self._graph_compiled = graph.compile()

    async def generate(self, user_letter: str) -> ...:
        inputs = {"user_letter": user_letter}
        async for event in self._graph_compiled.astream_events(inputs, version="v2"):
            event_type = event.get('event', None)
            agent = event.get('name', '')
            if agent in ["_write", "RunnableSequence", "__start__", "__end__", "LangGraph"]:
                continue
            if event_type == 'on_chat_model_stream':
                print(event['data']['chunk'].content, end='')
            elif event_type == 'on_chain_start':
                print(f"<{agent}>")
            elif event_type == 'on_chain_end':
                print(f"</{agent}>")


from langchain_gigachat import GigaChat
from src.config import settings


model = GigaChat(
    credentials=settings.giga_chat.api_key,
    scope=settings.giga_chat.scope,
    verify_ssl_certs=False,
    profanity_check=False
)

rewriter = RewriterNode(model)

agent = LettersAgent(rewriter_node=rewriter)

import asyncio

letter_1 = """
Тема: Задание
Здравствуйте,
Нужно сделать то, что я говорила на встрече. Все должно быть готово к следующей неделе. Не забудьте про детали.
Спасибо,Анна
"""

letter_2 = """
Тема: Апргрейд
Добрый день! 
Елена Александровна после апгрейда у вас перестал работать отчет по номенклатурным группам, срочно свяжитесь с нами для оперативного подключения к решению этой проблемы
"""


async def main() -> None:
    res = await agent.generate(letter_2)
    print(res)


asyncio.run(main())
