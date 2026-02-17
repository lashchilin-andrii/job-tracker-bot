from aiogram import Router, F
from aiogram.types import Message

from src.button import BUTTON_PROFILE

router = Router()


@router.message(F.text == BUTTON_PROFILE)
async def get_me(message: Message):
    user = message.from_user

    user_id = user.id
    username = user.username or "No username"
    first_name = user.first_name
    last_name = user.last_name or ""
    language = user.language_code or "Unknown"

    text = (
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"Name: {first_name} {last_name}\n"
        f"Lang: {language}"
    )

    await message.answer(text)
