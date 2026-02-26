from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.button import BUTTON_NEXT, BUTTON_PREVIOUS
from src.job.model import JobModel


def get_navigation_keyboard(
    current_index: int, jobs: list[JobModel], prefix: str
) -> list[list[InlineKeyboardButton]]:
    total = len(jobs)

    page_btn = InlineKeyboardButton(
        text=f"{current_index + 1}/{total}",
        callback_data="noop",
    )

    if current_index == 0:
        next_job = jobs[current_index + 1] if total > 1 else jobs[current_index]

        next_btn_1 = InlineKeyboardButton(
            text=BUTTON_NEXT,
            callback_data=f"{prefix}{next_job.job_id}",
        )

        next_btn_2 = InlineKeyboardButton(
            text=BUTTON_NEXT,
            callback_data=f"{prefix}{next_job.job_id}",
        )

        return [[next_btn_1, page_btn, next_btn_2]]

    if current_index == total - 1:
        prev_job = jobs[current_index - 1]

        prev_btn_1 = InlineKeyboardButton(
            text=BUTTON_PREVIOUS,
            callback_data=f"{prefix}{prev_job.job_id}",
        )

        prev_btn_2 = InlineKeyboardButton(
            text=BUTTON_PREVIOUS,
            callback_data=f"{prefix}{prev_job.job_id}",
        )

        return [[prev_btn_1, page_btn, prev_btn_2]]

    prev_job = jobs[current_index - 1]
    next_job = jobs[current_index + 1]

    prev_btn = InlineKeyboardButton(
        text=BUTTON_PREVIOUS,
        callback_data=f"{prefix}{prev_job.job_id}",
    )

    next_btn = InlineKeyboardButton(
        text=BUTTON_NEXT,
        callback_data=f"{prefix}{next_job.job_id}",
    )

    return [[prev_btn, page_btn, next_btn]]


def get_service_keyboard() -> list[list[InlineKeyboardButton]]:
    buttons = [
        InlineKeyboardButton(text="🫩", callback_data="noop"),
        InlineKeyboardButton(text="😪", callback_data="noop"),
    ]
    return [buttons]


def get_menu_keyboard(
    current_index: int, jobs: list[JobModel], prefix: str
) -> InlineKeyboardMarkup:
    keyboard_rows = []

    keyboard_rows += get_navigation_keyboard(current_index, jobs, prefix)

    keyboard_rows += get_service_keyboard()

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
