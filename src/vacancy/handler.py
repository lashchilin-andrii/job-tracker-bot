from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("vacancy"))
async def start_handler(message: Message):
    await message.answer("vacancies vacancies vacancies")
