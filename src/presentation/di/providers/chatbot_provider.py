from dishka import Provider, provide, Scope

from src.ai_agent import DIOAgent
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
            ai_agent: DIOAgent,
            dialog_repository: DialogRepository
    ) -> ChatBotUseCase:
        return ChatBotUseCase(ai_agent, dialog_repository)

    @provide(scope=Scope.APP)
    def get_chatbot_controller(self, chatbot: ChatBotUseCase) -> ChatBotController:
        return ChatBotController(chatbot)
