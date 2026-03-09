from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    user_name: str | None
    user_first_name: str | None
    user_last_name: str | None
    user_language: str

    @classmethod
    def from_telegram_user(cls, tg_user) -> "User":
        return cls(
            user_id=str(tg_user.id),
            user_name=tg_user.username,
            user_first_name=tg_user.first_name,
            user_last_name=tg_user.last_name,
            user_language=tg_user.language_code,
        )
