from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from src.button import BUTTON_NEXT, BUTTON_PREVIOUS
from src.job.model import JobModel


def get_navigation_keyboard(
    current_index: int, jobs: List[JobModel], prefix: str
) -> List[List[InlineKeyboardButton]]:
    buttons = []

    if current_index > 0:
        prev_job = jobs[current_index - 1]
        buttons.append(
            InlineKeyboardButton(
                text=BUTTON_PREVIOUS,
                callback_data=f"{prefix}{prev_job.job_id}",
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"{current_index + 1}/{len(jobs)}",
            callback_data="noop",
        )
    )

    if current_index < len(jobs) - 1:
        next_job = jobs[current_index + 1]
        buttons.append(
            InlineKeyboardButton(
                text=BUTTON_NEXT,
                callback_data=f"{prefix}{next_job.job_id}",
            )
        )

    return [buttons]


def get_service_keyboard() -> List[List[InlineKeyboardButton]]:
    buttons = [
        InlineKeyboardButton(text="row 2 btn 1", callback_data="noop"),
        InlineKeyboardButton(text="row 2 btn 2", callback_data="noop"),
    ]
    return [buttons]


def get_menu_keyboard(
    current_index: int, jobs: List[JobModel], prefix: str
) -> InlineKeyboardMarkup:
    keyboard_rows = []

    keyboard_rows += get_navigation_keyboard(current_index, jobs, prefix)

    keyboard_rows += get_service_keyboard()

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
