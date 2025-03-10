from dishka import Provider, provide, Scope

from src.database.sql_database_manager import SQLDatabaseManager
from src.database.crud import UserCRUD, DialogCRUD
from src.config import settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_database_manager(self) -> SQLDatabaseManager:
        return SQLDatabaseManager(settings.db.url)

    @provide(scope=Scope.APP)
    def get_user_crud(self, manager: SQLDatabaseManager) -> UserCRUD:
        return UserCRUD(manager)

    @provide(scope=Scope.APP)
    def get_dialog_crud(self, manager: SQLDatabaseManager) -> DialogCRUD:
        return DialogCRUD(manager)
