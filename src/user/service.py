from pathlib import Path
from aiogram.types import Message

from src.base.service import render_template
from src.user.schema import User
from src.user.model import UserModel
from src.user.repository import UserRepository
from src.user_job.service import get_user_jobs_stats_by_user_id


def get_or_create_user(user_raw) -> UserModel:
    user_id = str(user_raw.id)

    db_user = UserRepository().read_by_property("user_id", user_id)
    if db_user:
        return db_user

    return UserRepository().create_one(
        UserModel(
            user_id=user_id,
            user_name=user_raw.username,
            user_first_name=user_raw.first_name,
            user_last_name=user_raw.last_name,
            user_language=user_raw.language_code or "en",
        )
    )


async def show_profile(message: Message):
    user_raw = message.from_user

    db_user = get_or_create_user(user_raw)

    user = User(
        user_id=db_user.user_id,
        user_name=db_user.user_name,
        user_first_name=db_user.user_first_name,
        user_last_name=db_user.user_last_name,
        user_language=db_user.user_language,
    )

    stats = get_user_jobs_stats_by_user_id(str(user_raw.id))

    await message.answer(
        render_template(
            template_path=Path(__file__).parent / "template" / "profile.html",
            username=user.user_name or "NoUsername",
            first_name=user.user_first_name or "",
            last_name=user.user_last_name or "",
            language=user.user_language or "en",
            stats=stats,
        )
    )
