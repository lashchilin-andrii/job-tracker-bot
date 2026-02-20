from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.button import BUTTON_JOBS
from src.job.keyboard import jobs_list_inline_kb

router = Router()


@router.message(F.text == BUTTON_JOBS)
async def start_handler(message: Message):
    await message.answer(
        "Here are some jobs for you:", reply_markup=jobs_list_inline_kb
    )


@router.callback_query(F.data.startswith("job_"))
async def job_callback_handler(callback: CallbackQuery):
    job_id = callback.data.split("_")[1]

    await callback.message.answer(f"You selected job ID: {job_id}")
    await callback.answer()
