from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.button import button_next, button_previous, button_save_job
from src.job.model import JobModel


def get_navigation_keyboard(
    current_index: int,
    jobs: list[JobModel],
    prefix: str,
) -> list[list[InlineKeyboardButton]]:

    total = len(jobs)

    prev_index = max(0, current_index - 1)
    next_index = min(total - 1, current_index + 1)

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
        text=f"{current_index + 1}/{total}",
        callback_data="noop",
    )

    return [[prev_btn, page_btn, next_btn]]


def get_service_keyboard() -> list[list[InlineKeyboardButton]]:

    save_btn = InlineKeyboardButton(
        text=button_save_job.text,
        callback_data=f"{button_save_job.callback_prefix}",
    )
    return [[save_btn]]


def get_menu_keyboard(
    current_index: int,
    jobs: list[JobModel],
    callback_prefix: str,
) -> InlineKeyboardMarkup:

    keyboard = []
    keyboard += get_navigation_keyboard(current_index, jobs, callback_prefix)
    keyboard += get_service_keyboard()

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
