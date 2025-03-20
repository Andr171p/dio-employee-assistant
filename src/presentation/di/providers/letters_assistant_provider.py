from dishka import Provider, provide, Scope

from langchain_core.language_models import BaseChatModel, LLM

from src.utils import FileSaver
from src.services import LettersService
from src.ai_agent import BaseAgent, LettersAgent
from src.core.use_cases import LettersAssistantUseCase


class LettersAssistantProvider(Provider):
    @provide(scope=Scope.APP)
    def get_file_saver(self) -> FileSaver:
        return FileSaver()

    @provide(scope=Scope.APP)
    def get_letters_service(self, file_saver: FileSaver) -> LettersService:
        return LettersService(file_saver)

    @provide(scope=Scope.APP)
    def get_agent(self, model: BaseChatModel | LLM) -> BaseAgent:
        return LettersAgent(model)

    @provide(scope=Scope.APP)
    def get_letters_assistant_use_case(
            self,
            ai_agent: BaseAgent,
            letters_service: LettersService
    ) -> LettersAssistantUseCase:
        return LettersAssistantUseCase(ai_agent, letters_service)
