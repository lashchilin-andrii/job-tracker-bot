from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.exceptions import Present
from src.message import MSG_SAVED_SUCCESSFULLY, MSG_OBJECT_EXISTS
from src.job.model import JobModel
from src.job.service import save_job
from src.job.state import CurrentJobState
from src.button import (
    button_save_job,
    button_my_jobs,
    button_change_job_status,
    button_delete_job,
)
from src.user_job.service import save_my_job

from src.user_job.service import (
    show_my_jobs,
    handle_my_jobs_callback,
    change_job_status,
    delete_job,
)
from src.user_job.schema import UserJob


router = Router()


@router.callback_query(F.data.startswith(button_save_job.callback_prefix))
async def save_my_job_handler(callback: CallbackQuery, state: FSMContext):
    """Save my job if not saved."""
    job: JobModel = await save_job(await CurrentJobState.get_job_data(state))
    try:
        await save_my_job(
            user_job=UserJob(user_id=str(callback.from_user.id), job_id=job.job_id)
        )
    except Present:
        await callback.answer(MSG_OBJECT_EXISTS, show_alert=True)
    await callback.answer(MSG_SAVED_SUCCESSFULLY, show_alert=True)


@router.message(F.text == button_my_jobs.text)
async def my_jobs_handler(message: Message, state: FSMContext):
    await show_my_jobs(message, state)


@router.callback_query(F.data.startswith(button_my_jobs.callback_prefix))
async def my_jobs_callback_handler(callback: CallbackQuery, state: FSMContext):
    await handle_my_jobs_callback(callback, state)


@router.callback_query(F.data.startswith(button_change_job_status.callback_prefix))
async def change_job_status_handler(callback: CallbackQuery, state: FSMContext):
    await change_job_status(callback, state)


@router.callback_query(F.data.startswith(button_delete_job.callback_prefix))
async def delete_job_handler(callback: CallbackQuery, state: FSMContext):
    await delete_job(callback, state)
