from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.base.button import ButtonBase
from src.button import button_next, button_previous
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


def get_service_keyboard(
    include_buttons: list[ButtonBase],
) -> list[list[InlineKeyboardButton]]:

    buttons = []
    for include_button in include_buttons:
        buttons.append(
            InlineKeyboardButton(
                text=include_button.text,
                callback_data=f"{include_button.callback_prefix}",
            )
        )
    return [buttons]


def get_menu_keyboard(
    current_index: int,
    jobs: list[JobModel],
    callback_prefix: str,
    include_buttons: list[ButtonBase],
) -> InlineKeyboardMarkup:

    keyboard = []
    keyboard += get_navigation_keyboard(current_index, jobs, callback_prefix)
    keyboard += get_service_keyboard(include_buttons=include_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
