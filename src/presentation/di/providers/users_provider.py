from dishka import Provider, provide, Scope

from src.database.crud import UserCRUD
from src.repository import UserRepository
from src.core.use_cases import UserUseCase


class UsersProvider(Provider):
    @provide(scope=Scope.APP)
    def get_user_repository(self, crud: UserCRUD) -> UserRepository:
        return UserRepository(crud)

    @provide(scope=Scope.APP)
    def get_user_use_case(self, repository: UserRepository) -> UserUseCase:
        return UserUseCase(repository)
