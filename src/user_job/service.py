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
    """Get all user_jobs objects by user_id."""
    user_jobs = UserJobRepository().read_all_by_property("user_id", str(user_id))

    if not user_jobs:
        raise Absent("You have not saved any jobs yet.")

    return user_jobs


def toggle_user_job_status(user_job: UserJob) -> UserJob:
    statuses = list(UserJobStatus)

    try:
        current_idx = next(
            i for i, s in enumerate(statuses) if s.value == user_job.user_job_status
        )
    except StopIteration:
        current_idx = 0

    new_status = statuses[(current_idx + 1) % len(statuses)].value
    user_job.user_job_status = new_status

    user_job_model = UserJobModel(
        user_id=user_job.user_id,
        job_id=user_job.job_id,
        user_job_status=user_job.user_job_status,
    )

    UserJobRepository().update_one(user_job_model)

    return user_job


async def delete_job(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    job: Job = await JobState.get_current_job_data(state)
    user_jobs: list[UserJob] = await JobState.get_user_jobs_data(state)
    jobs: list[Job] = await JobState.get_jobs_data(state)

    index = next((i for i, j in enumerate(jobs) if j.job_id == job.job_id), 0)
    user_job: UserJob = user_jobs[index]

    delete_user_job(user_job)

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


def delete_user_job(user_job: UserJob) -> None:
    """Delete a user_job by converting Pydantic model to SQLAlchemy model. Raises Absent if the object does not exist in DB."""
    db_obj = UserJobRepository().get_from_pydantic(user_job)
    if not db_obj:
        raise Absent("User job not found in database")
    UserJobRepository().delete_one(db_obj)
