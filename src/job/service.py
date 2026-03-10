import asyncio
from pathlib import Path

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from src.base.service import render_template
from src.job.repository import JobRepository
from src.job.schema import Job
from src.base.button import ButtonBase
from src.job.model import JobModel
from src.job.keyboard import get_job_menu_keyboard
from src.message import (
    MSG_NOT_FOUND,
    MSG_SESSION_EXPIRED,
)
from src.exceptions import Absent, InvalidCallbackData
from src.api.jooble import get_jobs
from src.state import JobState, JobSearchParametersState
from src.button import button_browse_jobs, button_save_job


def find_job_index(jobs: list[JobModel], job_id: str) -> int:
    for i, job in enumerate(jobs):
        if str(job.job_id) == job_id:
            return i
    raise InvalidCallbackData(MSG_NOT_FOUND)


async def show_job_page(
    callback: CallbackQuery,
    state: FSMContext,
    jobs: list[Job],
    button: ButtonBase,
):
    try:
        job_id = button.get_data_from_callback_without_prefix(callback.data)
        index = find_job_index(jobs, job_id)
        job = jobs[index]
    except InvalidCallbackData:
        await callback.message.answer(MSG_NOT_FOUND)
        return

    await state.set_state(JobState.current_job)
    await state.update_data(current_job=job)

    await callback.message.edit_text(
        render_template(
            template_path=Path(__file__).parent / "template" / "job.html", job=job
        ),
        parse_mode="HTML",
        reply_markup=get_job_menu_keyboard(
            jobs=jobs,
            callback_prefix=button.callback_prefix,
            include_buttons=[[button_save_job]],
            current_index=index,
        ),
    )


async def handle_browse_jobs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    jobs = await JobState.get_found_jobs_data(state)

    if not jobs:
        raise Absent(MSG_SESSION_EXPIRED)

    await show_job_page(
        callback,
        state,
        jobs,
        button_browse_jobs,
    )


async def process_location_step(message: Message, state: FSMContext):
    keywords = await JobSearchParametersState.get_keywords(state)
    location = message.text

    await message.answer(f"Keywords: {keywords}\nLocation: {location}")

    jobs = await asyncio.to_thread(get_jobs, keywords, location)

    if not jobs:
        raise Absent("No jobs.")

    await state.update_data(found_jobs=jobs)

    await state.set_state(JobState.current_job)
    await state.update_data(current_job=jobs[0])

    await message.answer(
        render_template(
            template_path=Path(__file__).parent / "template" / "job.html", job=jobs[0]
        ),
        parse_mode="HTML",
        reply_markup=get_job_menu_keyboard(
            jobs=jobs,
            callback_prefix=button_browse_jobs.callback_prefix,
            include_buttons=[[button_save_job]],
        ),
    )


async def save_job(job: Job | None) -> Job:
    """Save job if not exists."""
    if not job:
        raise Absent("No job in save_job")
    job_model = JobModel(**job.model_dump())

    try:
        return Job.model_validate(JobRepository().create_one(job_model).__dict__)
    except IntegrityError:
        return Job.model_validate(
            JobRepository().read_one_by_property("job_id", job_model.job_id).__dict__
        )


def get_jobs_by_ids(job_ids: list[str]) -> list[Job]:
    """Get list of Job object from db by their ids."""
    jobs = [
        Job.model_validate(job.__dict__)
        for job_id in job_ids
        if (job := JobRepository().read_one_by_property("job_id", job_id))
    ]
    if not jobs:
        raise Absent("No jobs found for provided job IDs.")
    return jobs
