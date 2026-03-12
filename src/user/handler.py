from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message

from src.base.service import render_template
from src.user_job.service import get_user_job_stats
from src.button import button_profile
from src.user.schema import User

router = Router()
TEMPLATE_PATH = Path(__file__).parent / "template" / "profile.html"


@router.message(F.text == button_profile.text)
async def profile_handler(message: Message):
    user = User.from_telegram_user(message.from_user)

    stats = get_user_job_stats(user.user_id)

    await message.answer(
        render_template(
            template_path=TEMPLATE_PATH,
            username=user.user_name,
            first_name=user.user_first_name,
            last_name=user.user_last_name,
            language=user.user_language,
            stats=stats,
        ),
        parse_mode="HTML",
    )
