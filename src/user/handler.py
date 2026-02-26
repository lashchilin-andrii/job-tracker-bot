from aiogram import Router, F
from aiogram.types import Message

from src.button import BUTTON_PROFILE
from src.user.service import render_profile, get_or_create_user

router = Router()


@router.message(F.text == BUTTON_PROFILE)
async def profile_handler(message: Message):
    user_raw = message.from_user
    get_or_create_user(user_raw)
    await message.answer(render_profile(user_raw=user_raw))
