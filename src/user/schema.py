from pydantic import BaseModel, field_validator


class User(BaseModel):
    user_id: str
    user_name: str | None
    user_first_name: str | None
    user_last_name: str | None
    user_language: str

    @field_validator("user_id", mode="before")
    @classmethod
    def convert_user_id_to_str(cls, v: str):
        return str(v)
