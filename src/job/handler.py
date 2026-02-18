from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("job"))
async def start_handler(message: Message):
    await message.answer("Job\nJob\nJob\nJob\nJob\nJob")
