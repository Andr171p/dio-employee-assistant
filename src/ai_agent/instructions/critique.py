from pydantic import BaseModel, Field


class Critique(BaseModel):
    thoughts: str = Field(description="Мысли по поводу ответа")
    critique: str = Field(description="Конструктивная критика ответа - что нужно поправить или доработать")
    search_query: str = Field(description="Текст поискового запроса на поиск данных по базе знаний, если нужен")
    final_decision: str = Field(description="Итоговое решение, должно быть одно из следующих: good (если нет новой критики), search (требуется поиск данных в базе знаний), fix (если требуется переписать или доработать ответ)")
