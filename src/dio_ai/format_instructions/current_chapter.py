from pydantic import BaseModel, Field


class CurrentChapter(BaseModel):
    chapter: str = Field(description="Итоговое решение, должно быть одно из следующих: ")
