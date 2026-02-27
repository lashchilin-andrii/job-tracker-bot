import asyncio
from pathlib import Path
from jinja2 import Template

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.job.repository import JobRepository
from src.job.model import JobModel
from src.job.keyboard import get_menu_keyboard
from src.job.message import (
    MSG_NO_JOBS_FOUND,
    MSG_JOB_NOT_FOUND,
    MSG_SESSION_EXPIRED,
    MSG_ENTER_KEYWORDS,
    MSG_ENTER_LOCATION,
)
from src.exceptions import InvalidCallbackData
from src.api.jooble import get_jobs
from src.job.state import JobState
from src.button import button_my_jobs, button_browse_jobs


def get_saved_jobs() -> list[JobModel]:
    return JobRepository().read_all()


def get_job_id_from_callback(data: str | None) -> str:
    if not data:
        raise InvalidCallbackData("Callback data is empty")

    try:
        job_id = data.split("_", 1)[-1]
    except ValueError:
        raise InvalidCallbackData("Invalid callback format")

    if not job_id:
        raise InvalidCallbackData("Invalid job callback")

    return job_id


def find_job_index(jobs: list[JobModel], job_id: str) -> int:
    for i, job in enumerate(jobs):
        if str(job.job_id) == job_id:
            return i
    raise InvalidCallbackData("Job not found")


def render_job(job: JobModel) -> str:
    template_path = Path(__file__).parent / "template" / "job.html"

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(job=job)


async def show_saved_jobs(message: Message):
    jobs = get_saved_jobs()

    if not jobs:
        await message.answer(MSG_NO_JOBS_FOUND)
        return

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(0, jobs, prefix=button_my_jobs.callback),
    )


async def handle_saved_job_callback(callback: CallbackQuery):
    await callback.answer()

    jobs = get_saved_jobs()

    try:
        job_id = get_job_id_from_callback(
            callback.data.replace(button_my_jobs.callback, "")
        )
        index = find_job_index(jobs, job_id)
        job = jobs[index]
    except InvalidCallbackData:
        await callback.message.answer(MSG_JOB_NOT_FOUND)
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(index, jobs, prefix=button_my_jobs.callback),
    )


async def handle_browse_jobs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    jobs = data.get("found_jobs")

    if not jobs:
        await callback.message.answer(MSG_SESSION_EXPIRED)
        return

    try:
        job_id = get_job_id_from_callback(callback.data)
        index = find_job_index(jobs, job_id)
        job = jobs[index]
    except InvalidCallbackData:
        await callback.message.answer(MSG_JOB_NOT_FOUND)
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(index, jobs, prefix=button_browse_jobs.callback),
    )


async def start_job_search(message: Message, state: FSMContext):
    await state.set_state(JobState.keywords)
    await message.answer(MSG_ENTER_KEYWORDS)


async def process_keywords_step(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await state.set_state(JobState.location)

    await message.answer(MSG_ENTER_LOCATION)


async def process_location_step(message: Message, state: FSMContext):
    data = await state.get_data()
    keywords = data["keywords"]
    location = message.text

    await message.answer(f"Keywords: {keywords}\nLocation: {location}")

    jobs = await asyncio.to_thread(get_jobs, keywords, location)

    if not jobs:
        await message.answer(MSG_NO_JOBS_FOUND)
        return

    await state.update_data(found_jobs=jobs)

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(0, jobs, prefix=button_browse_jobs.callback),
    )
    await state.set_state(None)
