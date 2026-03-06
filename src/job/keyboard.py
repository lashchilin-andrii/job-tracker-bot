from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.job.model import JobModel
from src.base.button import ButtonBase
from src.button import button_previous, button_next
from src.base.keyboard import get_keyboard_with_buttons


def get_job_navigation_keyboard(
    jobs: list[JobModel],
    current_index: int,
    callback_prefix: str,
) -> list[list[InlineKeyboardButton]]:
    """One line of buttons prev / page / next"""
    total = len(jobs)
    prev_index = (current_index - 1) % total
    next_index = (current_index + 1) % total

    return [
        [
            InlineKeyboardButton(
                text=button_previous.text,
                callback_data=f"{callback_prefix}{jobs[prev_index].job_id}",
            ),
            InlineKeyboardButton(
                text=f"{current_index + 1}/{total}", callback_data="noop"
            ),
            InlineKeyboardButton(
                text=button_next.text,
                callback_data=f"{callback_prefix}{jobs[next_index].job_id}",
            ),
        ]
    ]


def get_job_menu_keyboard(
    jobs: list[JobModel],
    current_index: int = 0,
    callback_prefix: str = "",
    include_buttons: list[list[ButtonBase]] = [[]],
) -> InlineKeyboardMarkup:

    keyboard = get_job_navigation_keyboard(jobs, current_index, callback_prefix)
    keyboard += get_keyboard_with_buttons(include_buttons)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
