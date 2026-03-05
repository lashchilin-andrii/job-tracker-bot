from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.base.button import ButtonBase
from src.button import button_next, button_previous
from src.job.model import JobModel
from src.base.keyboard import get_keyboard_with_buttons


def get_job_navigation_keyboard(
    current_job_index: int,
    jobs: list[JobModel],
    prefix: str,
) -> list[list[InlineKeyboardButton]]:

    total = len(jobs)

    prev_index = max(0, current_job_index - 1)
    next_index = min(total - 1, current_job_index + 1)

    prev_job = jobs[prev_index]
    next_job = jobs[next_index]

    prev_btn = InlineKeyboardButton(
        text=button_previous.text,
        callback_data=f"{prefix}{prev_job.job_id}",
    )

    next_btn = InlineKeyboardButton(
        text=button_next.text,
        callback_data=f"{prefix}{next_job.job_id}",
    )

    page_btn = InlineKeyboardButton(
        text=f"{current_job_index + 1}/{total}",
        callback_data="noop",
    )

    return [[prev_btn, page_btn, next_btn]]


def get_menu_keyboard(
    jobs: list[JobModel],
    callback_prefix: str,
    include_buttons: list[list[ButtonBase]] = [[]],
    current_job_index: int = 0,
) -> InlineKeyboardMarkup:

    keyboard = []
    keyboard += get_job_navigation_keyboard(current_job_index, jobs, callback_prefix)
    keyboard += get_keyboard_with_buttons(include_buttons=include_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
