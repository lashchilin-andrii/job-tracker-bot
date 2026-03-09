import asyncio
from pathlib import Path
from jinja2 import Template

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.base.button import ButtonBase
from src.job.model import JobModel
from src.job.keyboard import get_job_menu_keyboard
from src.message import (
    MSG_NOT_FOUND,
    MSG_SESSION_EXPIRED,
    MSG_ENTER_KEYWORDS,
    MSG_ENTER_LOCATION,
)
from src.exceptions import InvalidCallbackData
from src.api.jooble import get_jobs
from src.job.state import CurrentJobState, JobSearchParametersState
from src.button import button_browse_jobs, button_save_job


template_path = Path(__file__).parent / "template" / "job.html"


def find_job_index(jobs: list[JobModel], job_id: str) -> int:
    for i, job in enumerate(jobs):
        if str(job.job_id) == job_id:
            return i
    raise InvalidCallbackData(MSG_NOT_FOUND)


def render_job(job: JobModel) -> str:
    with open(template_path, "r", encoding="utf-8") as f:
        job_template = Template(f.read())
    return job_template.render(job=job)


async def show_job_page(
    callback: CallbackQuery,
    state: FSMContext,
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

    await state.set_state(CurrentJobState.job)
    await state.update_data(job=job)

    await callback.message.edit_text(
        render_job(job),
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

    data = await state.get_data()
    jobs = data.get("found_jobs")

    if not jobs:
        await callback.message.answer(MSG_SESSION_EXPIRED)
        return

    await show_job_page(
        callback,
        state,
        jobs,
        button_browse_jobs,
    )


async def start_job_search(message: Message, state: FSMContext):
    await state.set_state(JobSearchParametersState.keywords)
    await message.answer(MSG_ENTER_KEYWORDS)


async def process_keywords_step(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await state.set_state(JobSearchParametersState.location)
    await message.answer(MSG_ENTER_LOCATION)


async def process_location_step(message: Message, state: FSMContext):
    data = await state.get_data()

    keywords = data.get("keywords")
    location = message.text

    await message.answer(f"Keywords: {keywords}\nLocation: {location}")

    jobs = await asyncio.to_thread(get_jobs, keywords, location)

    if not jobs:
        await message.answer(MSG_NOT_FOUND)
        return

    await state.update_data(found_jobs=jobs)

    await state.set_state(CurrentJobState.job)
    await state.update_data(job=jobs[0].model_dump())

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_job_menu_keyboard(
            jobs=jobs,
            callback_prefix=button_browse_jobs.callback_prefix,
            include_buttons=[[button_save_job]],
        ),
    )
