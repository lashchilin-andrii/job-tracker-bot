from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.job.model import JobModel
from src.button import button_previous, button_next


def get_user_job_menu_keyboard(
    jobs: list[JobModel], current_job_id: str, callback_prefix: str
) -> InlineKeyboardMarkup:
    current_index = next(
        (i for i, job in enumerate(jobs) if str(job.job_id) == current_job_id), 0
    )
    total = len(jobs)
    prev_index = max(0, current_index - 1)
    next_index = min(total - 1, current_index + 1)

    keyboard = [
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

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
