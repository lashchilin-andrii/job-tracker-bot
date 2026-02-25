from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import asyncio

from src.button import BUTTON_GET_A_JOB, BUTTON_SAVED_JOBS
from src.job.service import (
    get_saved_jobs,
    get_job_id_from_callback,
    render_job,
)
from src.job.keyboard import get_navigation_keyboard
from src.exceptions import InvalidCallbackData
from src.api.jooble import get_jobs
from src.job.state import JobState

router = Router()


@router.message(F.text == BUTTON_SAVED_JOBS)
async def saved_jobs_handler(message: Message):
    jobs = get_saved_jobs()
    if not jobs:
        await message.answer("No jobs found.")
        return

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_navigation_keyboard(0, jobs, prefix="saved_job_"),
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
        await callback.message.answer("Job not found or invalid request.")
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_navigation_keyboard(index, jobs, prefix="saved_job_"),
    )


@router.callback_query(F.data.startswith("job_"))
async def get_a_job_callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    jobs = data.get("found_jobs")
    if not jobs:
        await callback.message.answer("Session expired. Please search again.")
        return

    try:
        job_id = get_job_id_from_callback(callback.data)
        index = next(i for i, j in enumerate(jobs) if str(j.job_id) == job_id)
        job = jobs[index]
    except (InvalidCallbackData, StopIteration):
        await callback.message.answer("Job not found or invalid request.")
        return

    await callback.message.edit_text(
        render_job(job),
        parse_mode="HTML",
        reply_markup=get_navigation_keyboard(index, jobs, prefix="job_"),
    )


@router.message(F.text == BUTTON_GET_A_JOB)
async def get_a_job_handler(message: Message, state: FSMContext):
    await state.set_state(JobState.keywords)
    await message.answer("Enter keywords (example: python backend):")


@router.message(JobState.keywords)
async def process_keywords(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await state.set_state(JobState.location)
    await message.answer("Enter location (example: Remote, USA, Germany):")


@router.message(JobState.location)
async def process_location(message: Message, state: FSMContext):
    data = await state.get_data()
    keywords = data["keywords"]
    location = message.text

    await message.answer("Searching...")

    jobs = await asyncio.to_thread(get_jobs, keywords, location)
    if not jobs:
        await message.answer("No jobs found.")
        return

    await state.update_data(found_jobs=jobs)

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_navigation_keyboard(0, jobs, prefix="job_"),
    )
