from pydantic import BaseModel
from uuid import UUID


class Vacancy(BaseModel):
    vacancy_id: UUID
    vacancy_name: str
