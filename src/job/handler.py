import asyncio
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.job.keyboard import get_job_menu_keyboard
from src.base.service import render_template
from src.exceptions import Absent, InvalidCallbackData
from src.message import MSG_ENTER_KEYWORDS, MSG_ENTER_LOCATION
from src.button import button_browse_jobs, button_save_job
from src.state import JobSearchParametersState, JobState
from src.api.jooble import get_jobs

router = Router()


@router.callback_query(F.data.startswith(button_browse_jobs.callback_prefix))
async def browse_jobs_callback_handler(callback: CallbackQuery, state: FSMContext):
    try:
        jobs = await JobState.get_found_jobs_data(state)
    except Absent as e:
        await callback.message.answer(str(e))
        return

    try:
        job_id = button_browse_jobs.get_data_from_callback_without_prefix(callback.data)
        index = next(
            (i for i, job in enumerate(jobs) if str(job.job_id) == job_id), None
        )
        job = jobs[index]
    except InvalidCallbackData as e:
        await callback.message.answer(str(e))
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
            callback_prefix=button_browse_jobs.callback_prefix,
            include_buttons=[[button_save_job]],
            current_index=index,
        ),
    )


@router.message(F.text == button_browse_jobs.text)
async def browse_jobs_handler(message: Message, state: FSMContext):
    await state.set_state(JobSearchParametersState.keywords)
    await message.answer(MSG_ENTER_KEYWORDS)


@router.message(JobSearchParametersState.keywords)
async def process_keywords(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await state.set_state(JobSearchParametersState.location)
    await message.answer(MSG_ENTER_LOCATION)


@router.message(JobSearchParametersState.location)
async def process_location(message: Message, state: FSMContext):
    keywords = await JobSearchParametersState.get_keywords(state)
    location = message.text

    await message.answer(f"Keywords: {keywords}\nLocation: {location}")

    try:
        jobs = await asyncio.to_thread(get_jobs, keywords, location)
    except Absent as e:
        await message.answer(str(e))
        return

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
