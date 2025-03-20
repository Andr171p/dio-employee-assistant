from pydantic import BaseModel


class AILetter(BaseModel):
    critique: str
    rewritten_letter: str
