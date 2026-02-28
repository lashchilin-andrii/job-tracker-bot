from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.button import button_browse_jobs, button_my_jobs
from src.job.service import (
    show_my_jobs,
    handle_my_jobs_callback,
    handle_browse_jobs_callback,
    start_job_search,
    process_keywords_step,
    process_location_step,
)
from src.job.state import JobState

router = Router()


@router.message(F.text == button_my_jobs.text)
async def my_jobs_handler(message: Message):
    await show_my_jobs(message)


@router.callback_query(F.data.startswith(button_my_jobs.callback_prefix))
async def my_jobs_callback_handler(callback: CallbackQuery):
    await handle_my_jobs_callback(callback)


@router.callback_query(F.data.startswith(button_browse_jobs.callback_prefix))
async def browse_jobs_callback_handler(callback: CallbackQuery, state: FSMContext):
    await handle_browse_jobs_callback(callback, state)


@router.message(F.text == button_browse_jobs.text)
async def browse_jobs_handler(message: Message, state: FSMContext):
    await start_job_search(message, state)


@router.message(JobState.keywords)
async def process_keywords(message: Message, state: FSMContext):
    await process_keywords_step(message, state)


@router.message(JobState.location)
async def process_location(message: Message, state: FSMContext):
    await process_location_step(message, state)
