from aiogram import Router, F
from aiogram.types import Message

from src.button import button_profile
from src.user.service import show_profile

router = Router()


@router.message(F.text == button_profile.text)
async def profile_handler(message: Message):
    await show_profile(message)
