from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.job.schema import Job
from src.button import (
    button_previous,
    button_next,
    button_change_job_status,
    button_delete_job,
)


def get_user_job_menu_keyboard(
    jobs: list,
    current_job_id: str,
    callback_prefix: str,
    user_job,
) -> InlineKeyboardMarkup:
    index_map = get_job_index_map(jobs)
    current_index = index_map.get(str(current_job_id), 0)
    prev_index, next_index = get_adjacent_indices(current_index, len(jobs))

    keyboard = [
        [
            InlineKeyboardButton(
                text=button_previous.text,
                callback_data=f"{callback_prefix}{jobs[prev_index].job_id}",
            ),
            InlineKeyboardButton(
                text=f"{current_index + 1}/{len(jobs)}", callback_data="noop"
            ),
            InlineKeyboardButton(
                text=button_next.text,
                callback_data=f"{callback_prefix}{jobs[next_index].job_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=button_change_job_status.set_text(user_job.user_job_status),
                callback_data=button_change_job_status.callback_prefix,
            )
        ],
        [
            InlineKeyboardButton(
                text=button_delete_job.text,
                callback_data=button_delete_job.callback_prefix,
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_job_index_map(jobs: list[Job]) -> dict[str, int]:
    return {str(job.job_id): i for i, job in enumerate(jobs)}


def get_adjacent_indices(current_index: int, total: int) -> tuple[int, int]:
    prev_index = (current_index - 1) % total
    next_index = (current_index + 1) % total
    return prev_index, next_index
