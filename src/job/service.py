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
from src.job.state import CurrentJobState, JobSearchParametersState
from src.button import button_my_jobs, button_browse_jobs


# ================= TEMPLATE =================

template_path = Path(__file__).parent / "template" / "job.html"

with open(template_path, "r", encoding="utf-8") as f:
    job_template = Template(f.read())


# ================= HELPERS =================


def get_my_jobs() -> list[JobModel]:
    return JobRepository().read_all()


def find_job_index(jobs: list[JobModel], job_id: str) -> int:
    for i, job in enumerate(jobs):
        if str(job.job_id) == job_id:
            return i
    raise InvalidCallbackData(MSG_NOT_FOUND)


def render_job(job: JobModel) -> str:
    return job_template.render(job=job)


# ================= CORE PAGE RENDER =================


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

    # 🔥 сохраняем текущую работу полностью
    await state.set_state(CurrentJobState.job)
    await state.update_data(job=job)

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            index,
            jobs,
            callback_prefix=button.callback_prefix,
        ),
    )


# ================= MY JOBS =================


async def show_my_jobs(message: Message, state: FSMContext):
    jobs = get_my_jobs()

    if not jobs:
        await message.answer(MSG_NOT_FOUND)
        return

    # сохраняем первую работу
    await state.set_state(CurrentJobState.job)
    await state.update_data(job=jobs[0])

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            0,
            jobs,
            callback_prefix=button_my_jobs.callback_prefix,
        ),
    )


async def handle_my_jobs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    jobs = get_my_jobs()

    if not jobs:
        await callback.message.answer(MSG_NOT_FOUND)
        return

    await show_job_page(
        callback,
        state,
        jobs,
        button_my_jobs,
    )


# ================= BROWSE JOBS =================


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


# ================= SEARCH FLOW =================


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

    # сохраняем найденные работы
    await state.update_data(found_jobs=jobs)

    # сохраняем первую как текущую
    await state.set_state(CurrentJobState.job)
    await state.update_data(job=jobs[0].model_dump())

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            0,
            jobs,
            callback_prefix=button_browse_jobs.callback_prefix,
        ),
    )
