from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    user_name: str | None
    user_first_name: str | None
    user_last_name: str | None
    user_language: str
