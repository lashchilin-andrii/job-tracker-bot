from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from collections import Counter
from pathlib import Path


from src.job.schema import Job
from src.exceptions import Absent, Present
from src.base.service import render_template
from src.user_job.keyboard import get_user_job_menu_keyboard
from src.user_job.schema import UserJob
from src.user_job.model import UserJobModel
from src.user_job.repository import UserJobRepository
from src.button import button_my_jobs
from src.state import JobState
from src.base.enum import UserJobStatus
from sqlalchemy.exc import IntegrityError


async def save_my_job(user_job: UserJob) -> UserJobModel:
    """Save user_job or raise exception."""
    try:
        return UserJobRepository().create_one(
            UserJobModel(
                user_id=user_job.user_id,
                job_id=user_job.job_id,
                user_job_status=UserJobStatus.applied.value,
            )
        )
    except IntegrityError:
        raise Present


def get_all_user_jobs_by_user_id(user_id: int | str) -> list[UserJobModel]:
    user_jobs = UserJobRepository().read_all_by_property("user_id", str(user_id))

    if not user_jobs:
        raise Absent("You have not saved any jobs yet.")

    return user_jobs


async def handle_my_jobs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    jobs: list[Job] = await JobState.get_jobs_data(state)
    user_jobs: list[UserJob] = await JobState.get_user_jobs_data(state)

    if not jobs:
        raise Absent("No such jobs saved.")

    job_id = button_my_jobs.get_data_from_callback_without_prefix(callback.data)

    index = next((i for i, j in enumerate(jobs) if str(j.job_id) == job_id), 0)

    job = jobs[index]
    user_job = user_jobs[index]

    await state.update_data(current_job=job)

    await callback.message.edit_text(
        render_template(
            template_path=Path(__file__).parent / "template" / "user_job.html",
            job=job,
            user_job=user_job,
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs=jobs,
            current_job_id=str(job.job_id),
            callback_prefix=button_my_jobs.callback_prefix,
            user_job=user_job,
        ),
    )


async def change_job_status(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    current_job: Job = await JobState.get_current_job_data(state)
    user_jobs: list[UserJob] = await JobState.get_user_jobs_data(state)
    jobs: list[Job] = await JobState.get_jobs_data(state)

    if not current_job or not jobs or not user_jobs:
        raise Absent

    index = next((i for i, j in enumerate(jobs) if j.job_id == current_job.job_id), 0)
    user_job = user_jobs[index]

    statuses = list(UserJobStatus)
    current_idx = next(
        (i for i, s in enumerate(statuses) if s.value == user_job.user_job_status), 0
    )
    new_status = statuses[(current_idx + 1) % len(statuses)].value

    user_job.user_job_status = new_status
    UserJobRepository().update_one(user_job)

    await state.update_data(current_job=current_job, user_jobs=user_jobs)

    await callback.message.edit_text(
        render_template(
            template_path=Path(__file__).parent / "template" / "user_job.html",
            job=current_job,
            user_job=user_job,
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs=jobs,
            current_job_id=str(current_job.job_id),
            callback_prefix=button_my_jobs.callback_prefix,
            user_job=user_job,
        ),
    )


async def delete_job(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    job: Job = await JobState.get_current_job_data(state)
    user_jobs: list[UserJob] = await JobState.get_user_jobs_data(state)
    jobs: list[Job] = await JobState.get_jobs_data(state)

    if not job or not jobs or not user_jobs:
        raise Absent

    index = next((i for i, j in enumerate(jobs) if j.job_id == job.job_id), 0)
    user_job = user_jobs[index]

    UserJobRepository().delete_one(user_job)

    del user_jobs[index]
    del jobs[index]

    if not jobs:
        await state.clear()
        raise Absent

    new_index = min(index, len(jobs) - 1)
    new_job = jobs[new_index]
    new_user_job = user_jobs[new_index]

    await state.update_data(current_job=new_job, jobs=jobs, user_jobs=user_jobs)

    await callback.message.edit_text(
        render_template(
            template_path=Path(__file__).parent / "template" / "user_job.html",
            job=new_job,
            user_job=new_user_job,
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs=jobs,
            current_job_id=str(new_job.job_id),
            callback_prefix=button_my_jobs.callback_prefix,
            user_job=new_user_job,
        ),
    )


def get_jobs_stats_by_user_id(user_id: str) -> dict:
    user_jobs = UserJobRepository().read_all_by_property("user_id", user_id) or []

    counter = Counter(uj.user_job_status for uj in user_jobs)

    stats = {status.value: counter.get(status.value, 0) for status in UserJobStatus}

    stats["total"] = len(user_jobs)

    return stats
