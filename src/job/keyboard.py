from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from src.button import BUTTON_NEXT, BUTTON_PREVIOUS
from src.job.model import JobModel


def get_navigation_keyboard(
    current_index: int, jobs: List[JobModel]
) -> InlineKeyboardMarkup:
    keyboard = []

    if current_index > 0:
        prev_job = jobs[current_index - 1]
        keyboard.append(
            InlineKeyboardButton(
                text=BUTTON_PREVIOUS, callback_data=f"job_{prev_job.job_id}"
            )
        )

    if current_index < len(jobs) - 1:
        next_job = jobs[current_index + 1]
        keyboard.append(
            InlineKeyboardButton(
                text=BUTTON_NEXT, callback_data=f"job_{next_job.job_id}"
            )
        )

    return InlineKeyboardMarkup(inline_keyboard=[keyboard])
