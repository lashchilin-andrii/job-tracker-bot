from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.job.model import JobModel
from src.user_job.model import UserJobModel
from src.button import button_previous, button_next, button_change_job_status


def get_user_job_menu_keyboard(
    jobs: list[JobModel],
    current_job_id: str,
    callback_prefix: str,
    user_job: UserJobModel,  # объект UserJob из БД
) -> InlineKeyboardMarkup:
    current_index = next(
        (i for i, job in enumerate(jobs) if str(job.job_id) == current_job_id), 0
    )
    total = len(jobs)
    prev_index = (current_index - 1) % total
    next_index = (current_index + 1) % total

    # Навигация
    keyboard = [
        [
            InlineKeyboardButton(
                text=button_previous.text,
                callback_data=f"{callback_prefix}{jobs[prev_index].job_id}",
            ),
            InlineKeyboardButton(
                text=f"{current_index + 1}/{total}",
                callback_data="noop",
            ),
            InlineKeyboardButton(
                text=button_next.text,
                callback_data=f"{callback_prefix}{jobs[next_index].job_id}",
            ),
        ]
    ]

    status_button = InlineKeyboardButton(
        text=button_change_job_status.set_text(user_job.user_job_status),
        callback_data=button_change_job_status.callback_prefix,
    )
    keyboard.append([status_button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
