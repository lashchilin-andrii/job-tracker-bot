import asyncio
from pathlib import Path
from jinja2 import Template

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.base.button import ButtonBase
from src.job.repository import JobRepository
from src.job.model import JobModel
from src.job.keyboard import get_menu_keyboard
from src.job.message import (
    MSG_NOT_FOUND,
    MSG_SESSION_EXPIRED,
    MSG_ENTER_KEYWORDS,
    MSG_ENTER_LOCATION,
)
from src.exceptions import InvalidCallbackData
from src.api.jooble import get_jobs
from src.job.state import JobState
from src.button import button_my_jobs, button_browse_jobs


template_path = Path(__file__).parent / "template" / "job.html"

with open(template_path, "r", encoding="utf-8") as f:
    job_template = Template(f.read())


def get_my_jobs() -> list[JobModel]:
    return JobRepository().read_all()


def find_job_index(jobs: list[JobModel], job_id: str) -> int:
    for i, job in enumerate(jobs):
        if str(job.job_id) == job_id:
            return i
    raise InvalidCallbackData(MSG_NOT_FOUND)


def render_job(job: JobModel) -> str:
    return job_template.render(job=job)


async def show_job_page(
    callback: CallbackQuery,
    jobs: list[JobModel],
    button: ButtonBase,
):
    try:
        job_id = button.get_data_from_callback_without_prefix(callback.data)
        index = find_job_index(jobs, job_id)
        job = jobs[index]
    except InvalidCallbackData:
        await callback.message.answer(MSG_NOT_FOUND)
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            index,
            jobs,
            callback_prefix=button.callback_prefix,
        ),
    )


async def show_my_jobs(message: Message):
    jobs = get_my_jobs()

    if not jobs:
        await message.answer(MSG_NOT_FOUND)
        return

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            0,
            jobs,
            callback_prefix=button_my_jobs.callback_prefix,
        ),
    )


async def handle_my_jobs_callback(callback: CallbackQuery):
    await callback.answer()

    jobs = get_my_jobs()

    await show_job_page(
        callback,
        jobs,
        button_my_jobs,
    )


async def handle_browse_jobs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    jobs = data.get("found_jobs")

    if not jobs:
        await callback.message.answer(MSG_SESSION_EXPIRED)
        return

    await show_job_page(
        callback,
        jobs,
        button_browse_jobs,
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
        await message.answer(MSG_NOT_FOUND)
        return

    await state.update_data(found_jobs=jobs)

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            0,
            jobs,
            callback_prefix=button_browse_jobs.callback_prefix,
        ),
    )

    await state.set_state(None)
