from pydantic import BaseModel, Field


class FirstStep(BaseModel):
    decision: str = Field(description="Итоговое решение, должно быть одно из следующих: ")
