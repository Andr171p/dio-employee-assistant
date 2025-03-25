from dishka import Provider, provide, Scope

from src.dio_ai_agent.agent import Agent
from src.database.crud import DialogCRUD
from src.repository import DialogRepository
from src.core.use_cases import ChatBotUseCase
from src.controllers import ChatBotController


class ChatBotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_dialog_repository(self, crud: DialogCRUD) -> DialogRepository:
        return DialogRepository(crud)

    @provide(scope=Scope.APP)
    def get_chatbot_use_case(
            self,
            ai_assistant: Agent,
            dialog_repository: DialogRepository
    ) -> ChatBotUseCase:
        return ChatBotUseCase(ai_assistant, dialog_repository)

    @provide(scope=Scope.APP)
    def get_chatbot_controller(self, chatbot: ChatBotUseCase) -> ChatBotController:
        return ChatBotController(chatbot)
