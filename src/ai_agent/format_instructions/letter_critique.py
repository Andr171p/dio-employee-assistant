from pydantic import BaseModel, Field


class LetterCritique(BaseModel):
    critique: str = Field(description="Конструктивная критика письма - что нужно поправить или доработать")
    rewritten_letter: str = Field(description="Переписанное письмо пользователя, согласно правилам")
