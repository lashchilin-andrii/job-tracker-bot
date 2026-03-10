from pathlib import Path
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.base.service import render_template
from src.exceptions import Present
from src.message import MSG_SAVED_SUCCESSFULLY, MSG_OBJECT_EXISTS
from src.job.model import JobModel
from src.job.service import get_jobs_by_ids, save_job
from src.state import JobState
from src.button import (
    button_save_job,
    button_my_jobs,
    button_change_job_status,
    button_delete_job,
)
from src.user_job.service import get_all_user_jobs_by_user_id, save_my_job

from src.user_job.service import (
    handle_my_jobs_callback,
    change_job_status,
    delete_job,
)
from src.user_job.schema import UserJob
from src.user_job.keyboard import get_user_job_menu_keyboard


router = Router()


@router.callback_query(F.data.startswith(button_save_job.callback_prefix))
async def save_my_job_handler(callback: CallbackQuery, state: FSMContext):
    """Save my job if not saved."""
    job: JobModel = await save_job(await JobState.get_current_job_data(state))
    try:
        await save_my_job(
            user_job=UserJob(user_id=str(callback.from_user.id), job_id=job.job_id)
        )
    except Present:
        await callback.answer(MSG_OBJECT_EXISTS, show_alert=True)
    await callback.answer(MSG_SAVED_SUCCESSFULLY, show_alert=True)


@router.message(F.text == button_my_jobs.text)
async def my_jobs_handler(message: Message, state: FSMContext):
    user_jobs = get_all_user_jobs_by_user_id(message.from_user.id)

    jobs = get_jobs_by_ids([uj.job_id for uj in user_jobs])

    await state.set_state(JobState.current_job)
    await state.update_data(
        current_job=jobs[0],
        user_jobs=user_jobs,
        jobs=jobs,
    )
    await message.answer(
        render_template(
            template_path=Path(__file__).parent / "template" / "user_job.html",
            job=jobs[0],
            user_job=user_jobs[0],
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs=jobs,
            current_job_id=str(jobs[0].job_id),
            callback_prefix=button_my_jobs.callback_prefix,
            user_job=user_jobs[0],
        ),
    )


@router.callback_query(F.data.startswith(button_my_jobs.callback_prefix))
async def my_jobs_callback_handler(callback: CallbackQuery, state: FSMContext):
    await handle_my_jobs_callback(callback, state)


@router.callback_query(F.data.startswith(button_change_job_status.callback_prefix))
async def change_job_status_handler(callback: CallbackQuery, state: FSMContext):
    await change_job_status(callback, state)


@router.callback_query(F.data.startswith(button_delete_job.callback_prefix))
async def delete_job_handler(callback: CallbackQuery, state: FSMContext):
    await delete_job(callback, state)
