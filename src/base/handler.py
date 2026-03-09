from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.message import MSG_PLEASE_CHOOSE_ACTION
from src.base.keyboard import main_keyboard
from src.user.service import create_user
from src.user.schema import User

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    create_user(
        user=User(
            user_id=message.from_user.id,
            user_name=message.from_user.username,
            user_first_name=message.from_user.first_name,
            user_last_name=message.from_user.last_name,
            user_language=message.from_user.language_code,
        )
    )
    await message.answer(MSG_PLEASE_CHOOSE_ACTION, reply_markup=main_keyboard)


@router.message(F.text)
async def any_text_handler(message: Message):
    await message.answer(MSG_PLEASE_CHOOSE_ACTION, reply_markup=main_keyboard)
