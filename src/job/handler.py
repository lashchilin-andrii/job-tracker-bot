from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio

from src.button import BUTTON_GET_A_JOB, BUTTON_SAVED_JOBS
from src.job.message import (
    MSG_NO_JOBS_FOUND,
    MSG_JOB_NOT_FOUND,
    MSG_SESSION_EXPIRED,
    MSG_ENTER_KEYWORDS,
    MSG_ENTER_LOCATION,
    MSG_SEARCHING,
)
from src.job.service import (
    get_saved_jobs,
    get_job_id_from_callback,
    render_job,
)
from src.job.keyboard import get_menu_keyboard
from src.exceptions import InvalidCallbackData
from src.api.jooble import get_jobs
from src.job.state import JobState

router = Router()


@router.message(F.text == BUTTON_SAVED_JOBS)
async def saved_jobs_handler(message: Message):
    jobs = get_saved_jobs()
    if not jobs:
        await message.answer(MSG_NO_JOBS_FOUND)
        return

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(0, jobs, prefix="saved_job_"),
    )


@router.callback_query(F.data.startswith("saved_job_"))
async def saved_job_callback_handler(callback: CallbackQuery):
    await callback.answer()

    jobs = get_saved_jobs()
    try:
        job_id = get_job_id_from_callback(callback.data.replace("saved_", ""))
        index = next(i for i, j in enumerate(jobs) if str(j.job_id) == job_id)
        job = jobs[index]
    except (InvalidCallbackData, StopIteration):
        await callback.message.answer(MSG_JOB_NOT_FOUND)
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(index, jobs, prefix="saved_job_"),
    )


@router.callback_query(F.data.startswith("job_"))
async def get_a_job_callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    jobs = data.get("found_jobs")
    if not jobs:
        await callback.message.answer(MSG_SESSION_EXPIRED)
        return

    try:
        job_id = get_job_id_from_callback(callback.data)
        index = next(i for i, j in enumerate(jobs) if str(j.job_id) == job_id)
        job = jobs[index]
    except (InvalidCallbackData, StopIteration):
        await callback.message.answer(MSG_JOB_NOT_FOUND)
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(index, jobs, prefix="job_"),
    )


@router.message(F.text == BUTTON_GET_A_JOB)
async def get_a_job_handler(message: Message, state: FSMContext):
    await state.set_state(JobState.keywords)
    await message.answer(MSG_ENTER_KEYWORDS)


@router.message(JobState.keywords)
async def process_keywords(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await state.set_state(JobState.location)
    await message.answer(MSG_ENTER_LOCATION)


@router.message(JobState.location)
async def process_location(message: Message, state: FSMContext):
    data = await state.get_data()
    keywords = data["keywords"]
    location = message.text

    await message.answer(MSG_SEARCHING)

    jobs = await asyncio.to_thread(get_jobs, keywords, location)
    if not jobs:
        await message.answer(MSG_NO_JOBS_FOUND)
        return

    await state.update_data(found_jobs=jobs)

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(0, jobs, prefix="job_"),
    )
