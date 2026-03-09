from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from collections import Counter
from pathlib import Path

from src.base.service import render_template
from src.job.model import JobModel
from src.user_job.keyboard import get_user_job_menu_keyboard
from src.job.repository import JobRepository
from src.user_job.model import UserJobModel
from src.user_job.repository import UserJobRepository
from src.button import button_my_jobs
from src.job.state import CurrentJobState
from src.job.message import MSG_NOT_FOUND
from src.base.enum import UserJobStatus


async def save_job(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    job_data = data.get("job")

    if not job_data:
        await callback.message.answer("❌ No job in state")
        return

    if isinstance(job_data, dict):
        job_dict = job_data
    else:
        job_dict = job_data.model_dump()

    job = JobModel(**job_dict)

    existing = JobRepository().read_by_property("job_id", job.job_id)
    if not existing:
        JobRepository().create_one(job)

    user_job = UserJobModel(
        user_id=str(callback.from_user.id),
        job_id=str(job.job_id),
        user_job_status=UserJobStatus.applied.value,
    )

    UserJobRepository().create_one(user_job)

    await callback.message.answer("✅ Job saved successfully")


async def show_my_jobs(message: Message, state: FSMContext):
    user_jobs = UserJobRepository().read_by_property(
        "user_id", str(message.from_user.id), read_all=True
    )

    if not user_jobs:
        await message.answer(MSG_NOT_FOUND)
        return

    jobs = [
        job
        for uj in user_jobs
        if (job := JobRepository().read_by_property("job_id", uj.job_id))
    ]

    if not jobs:
        await message.answer(MSG_NOT_FOUND)
        return

    await state.set_state(CurrentJobState.job)
    await state.update_data(
        job=jobs[0],
        user_jobs=user_jobs,
        jobs=jobs,
    )

    await message.answer(
        render_template(
            template_path=Path(__file__).parent / "template" / "user_job.html",
            job=jobs[0],
            user_job=user_jobs[0],
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs=jobs,
            current_job_id=str(jobs[0].job_id),
            callback_prefix=button_my_jobs.callback_prefix,
            user_job=user_jobs[0],
        ),
    )


async def handle_my_jobs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    jobs: list[JobModel] = data.get("jobs")
    user_jobs: list[UserJobModel] = data.get("user_jobs")

    if not jobs:
        await callback.message.answer(MSG_NOT_FOUND)
        return

    job_id = button_my_jobs.get_data_from_callback_without_prefix(callback.data)

    index = next((i for i, j in enumerate(jobs) if str(j.job_id) == job_id), 0)

    job = jobs[index]
    user_job = user_jobs[index]

    await state.update_data(job=job)

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
            user_job=user_job,  # передаём объект UserJob из БД
        ),
    )


async def change_job_status(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    job: JobModel = data.get("job")
    user_jobs: list[UserJobModel] = data.get("user_jobs")
    jobs: list[JobModel] = data.get("jobs")

    if not job or not jobs or not user_jobs:
        await callback.message.answer("❌ No job selected")
        return

    index = next((i for i, j in enumerate(jobs) if j.job_id == job.job_id), 0)
    user_job = user_jobs[index]

    statuses = list(UserJobStatus)
    current_idx = next(
        (i for i, s in enumerate(statuses) if s.value == user_job.user_job_status), 0
    )
    new_status = statuses[(current_idx + 1) % len(statuses)].value

    user_job.user_job_status = new_status
    UserJobRepository().update_one(user_job)

    await state.update_data(job=job, user_jobs=user_jobs)

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
            user_job=user_job,  # передаём объект UserJob для корректного текста кнопки
        ),
    )


async def delete_job(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    job: JobModel = data.get("job")
    user_jobs: list[UserJobModel] = data.get("user_jobs")
    jobs: list[JobModel] = data.get("jobs")

    if not job or not jobs or not user_jobs:
        await callback.message.answer("❌ No job selected")
        return

    index = next((i for i, j in enumerate(jobs) if j.job_id == job.job_id), 0)
    user_job = user_jobs[index]

    UserJobRepository().delete_one(user_job)

    del user_jobs[index]
    del jobs[index]

    if not jobs:
        await state.clear()
        return

    new_index = min(index, len(jobs) - 1)
    new_job = jobs[new_index]
    new_user_job = user_jobs[new_index]

    await state.update_data(job=new_job, jobs=jobs, user_jobs=user_jobs)

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


def get_user_jobs_stats_by_user_id(user_id: str) -> dict:
    user_jobs = (
        UserJobRepository().read_by_property("user_id", user_id, read_all=True) or []
    )

    counter = Counter(uj.user_job_status for uj in user_jobs)

    stats = {status.value: counter.get(status.value, 0) for status in UserJobStatus}

    stats["total"] = len(user_jobs)

    return stats
