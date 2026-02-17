from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.keyboard import main_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Please, choose action:", reply_markup=main_keyboard)
