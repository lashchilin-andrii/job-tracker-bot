from aiogram import Router, F
from aiogram.types import Message

from src.button import BUTTON_JOBS
from src.job.keyboard import jobs_list_kb

router = Router()


@router.message(F.text == BUTTON_JOBS)
async def start_handler(message: Message):
    await message.answer("Here are some jobs for you:", reply_markup=jobs_list_kb)
