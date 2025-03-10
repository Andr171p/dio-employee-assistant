from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from src.database.crud import DialogCRUD

from src.core.entities import Dialog
from src.database.models import DialogModel
from src.repository.base_repository import BaseRepository


class DialogRepository(BaseRepository):
    def __init__(self, crud: "DialogCRUD") -> None:
        self._crud = crud

    async def save(self, dialog: Dialog) -> int:
        id = await self._crud.create(DialogModel(**dialog.model_dump()))
        return id

    async def get_all(self) -> List[Union[Dialog, None]]:
        dialogs = await self._crud.read_all()
        return [Dialog.model_validate(dialog) for dialog in dialogs] if dialogs else []
