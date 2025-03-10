from dishka import Provider, provide, Scope

from src.database.sql_database_manager import DatabaseManager
from src.database.crud import UserCRUD, DialogCRUD, VoteCRUD
from src.config import settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_database_manager(self) -> DatabaseManager:
        return DatabaseManager(settings.db.url)

    @provide(scope=Scope.APP)
    def get_user_crud(self, manager: DatabaseManager) -> UserCRUD:
        return UserCRUD(manager)

    @provide(scope=Scope.APP)
    def get_dialog_crud(self, manager: DatabaseManager) -> DialogCRUD:
        return DialogCRUD(manager)

    @provide(scope=Scope.APP)
    def get_vote_crud(self, manager: DatabaseManager) -> VoteCRUD:
        return VoteCRUD(manager)
