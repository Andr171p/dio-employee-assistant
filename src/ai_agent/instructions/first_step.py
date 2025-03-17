from pydantic import BaseModel, Field


class FirstStep(BaseModel):
    search_query: str = Field(description="Текст поискового запроса на поиск данных в базе знаний")
    final_decision: str = Field(description="Итоговое решение, должно быть одно из следующих: ")
