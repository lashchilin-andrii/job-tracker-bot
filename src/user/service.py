from pathlib import Path
from jinja2 import Template
from src.user.schema import User
from src.user.model import UserModel
from src.user.repository import UserRepository


def get_or_create_user(user_raw) -> UserModel:
    """
    Получаем пользователя из базы по Telegram ID или создаём нового.
    """
    user_id = str(user_raw.id)

    db_user = UserRepository().read_one_by_property("user_id", user_id)
    if db_user:
        return db_user

    return UserRepository().create_one(
        UserModel(
            user_id=user_id,
            user_name=user_raw.user_name,
            user_first_name=user_raw.user_first_name,
            user_last_name=user_raw.user_last_name,
            user_language=user_raw.user_language or "en",
        )
    )


def render_profile(user_raw) -> str:
    user = User(
        user_id=user_raw.id,
        user_name=user_raw.username,
        user_first_name=user_raw.first_name,
        user_last_name=user_raw.last_name,
        user_language=user_raw.language_code,
    )

    template_path = Path(__file__).parent / "template" / "profile.html"

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(
        username=user.user_name or "NoUsername",
        first_name=user.user_first_name or "",
        last_name=user.user_last_name or "",
        language=user.user_language,
    ).strip()
