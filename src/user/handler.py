from aiogram import Router, F
from aiogram.types import Message


from src.button import BUTTON_PROFILE
from src.user.service import render_profile

router = Router()


@router.message(F.text == BUTTON_PROFILE)
async def profile_handler(message: Message):
    user = message.from_user

    await message.answer(render_profile(user_raw=user))
