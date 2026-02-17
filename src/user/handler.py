from aiogram import Router, F
from aiogram.types import Message
from uuid import uuid4


from src.button import BUTTON_PROFILE
from src.user.schema import User
from src.user.service import user_to_str

router = Router()


@router.message(F.text == BUTTON_PROFILE)
async def get_me(message: Message):
    user_raw = message.from_user

    user = User(
        user_id=uuid4(),
        user_name=user_raw.username,
        user_first_name=user_raw.first_name,
        user_last_name=user_raw.last_name,
        user_language=user_raw.language_code,
    )

    await message.answer(user_to_str(user=user))
