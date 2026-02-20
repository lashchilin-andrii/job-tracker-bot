from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.button import BUTTON_SAVED_JOBS
from src.job.service import (
    get_all_jobs,
    get_job_id_from_callback,
    render_job,
)
from src.job.keyboard import get_navigation_keyboard
from src.exceptions import InvalidCallbackData

router = Router()

jobs = get_all_jobs()


@router.message(F.text == BUTTON_SAVED_JOBS)
async def start_handler(message: Message):
    if not jobs:
        await message.answer("No jobs found.")
        return

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_navigation_keyboard(0, jobs),
    )


@router.callback_query(F.data.startswith("job_"))
async def job_callback_handler(callback: CallbackQuery):
    try:
        job_id = get_job_id_from_callback(callback.data)
    except InvalidCallbackData:
        await callback.answer("Invalid request", show_alert=True)
        return

    try:
        index = next(i for i, j in enumerate(jobs) if str(j.job_id) == job_id)
        job = jobs[index]
    except StopIteration:
        await callback.answer("Job not found", show_alert=True)
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_navigation_keyboard(index, jobs),
    )

    await callback.answer()
