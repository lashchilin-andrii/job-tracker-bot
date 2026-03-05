from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.button import button_save_job, button_my_jobs
from src.user_job.service import save_job

from src.user_job.service import (
    show_my_jobs,
    handle_my_jobs_callback,
)

router = Router()


@router.callback_query(F.data.startswith(button_save_job.callback_prefix))
async def save_job_handler(callback: CallbackQuery, state: FSMContext):
    await save_job(callback, state)


@router.message(F.text == button_my_jobs.text)
async def my_jobs_handler(message: Message, state: FSMContext):
    await show_my_jobs(message, state)


@router.callback_query(F.data.startswith(button_my_jobs.callback_prefix))
async def my_jobs_callback_handler(callback: CallbackQuery, state: FSMContext):
    await handle_my_jobs_callback(callback, state)
