from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.job.model import JobModel


def get_jobs_keyboard(jobs: list[JobModel]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=job.job_name,
                    callback_data=f"job_{job.job_id}",
                )
            ]
            for job in jobs
        ]
    )
