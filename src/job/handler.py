from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.button import BUTTON_SAVED_JOBS
from src.job.service import (
    get_all_jobs,
    get_job_id_from_callback,
    get_job_by_id,
)
from src.job.keyboard import get_jobs_keyboard

router = Router()


@router.message(F.text == BUTTON_SAVED_JOBS)
async def start_handler(message: Message):
    jobs = get_all_jobs()

    if not jobs:
        await message.answer("No jobs found.")
        return

    keyboard = get_jobs_keyboard(jobs)

    await message.answer("Your saved jobs:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("job_"))
async def job_callback_handler(callback: CallbackQuery):
    job_id = get_job_id_from_callback(callback.data)

    job = get_job_by_id(job_id)

    if not job:
        await callback.answer("Job not found", show_alert=True)
        return

    await callback.message.answer(
        f"{job.job_name}\n"
        f"Company: {job.job_company or '-'}\n"
        f"Location: {job.job_location or '-'}\n"
        f"Salary: {job.job_salary or '-'}"
    )

    await callback.answer()
