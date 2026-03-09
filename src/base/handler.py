from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.message import MSG_PLEASE_CHOOSE_ACTION
from src.base.keyboard import main_keyboard
from src.user.service import create_user

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    create_user(message=message)
    await message.answer(MSG_PLEASE_CHOOSE_ACTION, reply_markup=main_keyboard)


@router.message(F.text)
async def any_text_handler(message: Message):
    await message.answer(MSG_PLEASE_CHOOSE_ACTION, reply_markup=main_keyboard)
