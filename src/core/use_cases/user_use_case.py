from src.core.entities import User, Vote
from src.repository import UserRepository


class UserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def register(self, user: User) -> None:
        await self._user_repository.save(user)
