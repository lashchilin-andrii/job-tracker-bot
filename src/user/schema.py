from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    user_id: UUID
    user_name: str | None
    user_first_name: str | None
    user_last_name: str | None
    user_language: str

