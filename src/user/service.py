from pathlib import Path
from jinja2 import Template
from src.user.schema import User


def render_profile(user_raw) -> str:
    user = User(
        user_id="1",
        user_name=user_raw.username,
        user_first_name=user_raw.first_name,
        user_last_name=user_raw.last_name,
        user_language=user_raw.language_code,
    )

    trmplate_path = Path(__file__).parent / "template" / "profile.html"
    with open(trmplate_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(
        username=user.user_name or "NoUsername",
        first_name=user.user_first_name or "",
        last_name=user.user_last_name or "",
        language=user.user_language,
    )
