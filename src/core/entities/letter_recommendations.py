from pydantic import BaseModel


class LetterRecommendation(BaseModel):
    critique: str
    rewritten_letter: str
