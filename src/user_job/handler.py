from pathlib import Path
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.job.schema import Job
from src.user_job.schema import UserJob
from src.base.service import render_template
from src.exceptions import Absent, Present
from src.message import MSG_SAVED_SUCCESSFULLY, MSG_OBJECT_EXISTS
from src.state import JobState
from src.job.service import get_jobs_by_ids, save_job
from src.user_job.service import (
    delete_user_job,
    get_all_user_jobs_by_user_id,
    save_my_job,
    toggle_user_job_status,
)
from src.user_job.keyboard import get_user_job_menu_keyboard
from src.button import (
    button_save_job,
    button_my_jobs,
    button_change_job_status,
    button_delete_job,
)

router = Router()
TEMPLATE_PATH = Path(__file__).parent / "template" / "user_job.html"


@router.callback_query(F.data.startswith(button_save_job.callback_prefix))
async def save_my_job_handler(callback: CallbackQuery, state: FSMContext):
    job: Job = await save_job(await JobState.get_current_job_data(state))
    try:
        await save_my_job(
            UserJob(user_id=str(callback.from_user.id), job_id=job.job_id)
        )
    except Present:
        await callback.answer(MSG_OBJECT_EXISTS, show_alert=True)
        return
    await callback.answer(MSG_SAVED_SUCCESSFULLY, show_alert=True)


@router.message(F.text == button_my_jobs.text)
async def my_jobs_handler(message: Message, state: FSMContext):
    try:
        user_jobs = get_all_user_jobs_by_user_id(message.from_user.id)
    except Absent as e:
        await message.answer(str(e))
        return

    jobs = get_jobs_by_ids([uj.job_id for uj in user_jobs])

    await state.set_state(JobState.current_job)
    await state.update_data(current_job=jobs[0], jobs=jobs, user_jobs=user_jobs)

    text = render_template(
        template_path=TEMPLATE_PATH, job=jobs[0], user_job=user_jobs[0]
    )
    keyboard = get_user_job_menu_keyboard(
        jobs=jobs,
        current_job_id=str(jobs[0].job_id),
        callback_prefix=button_my_jobs.callback_prefix,
        user_job=user_jobs[0],
    )
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data.startswith(button_my_jobs.callback_prefix))
async def my_jobs_callback_handler(callback: CallbackQuery, state: FSMContext):
    jobs: list[Job] = await JobState.get_jobs_data(state)
    user_jobs: list[UserJob] = await JobState.get_user_jobs_data(state)

    job_id = button_my_jobs.get_data_from_callback_without_prefix(callback.data)
    index = next((i for i, j in enumerate(jobs) if str(j.job_id) == job_id), 0)

    await state.update_data(current_job=jobs[index])

    await callback.message.edit_text(
        render_template(
            template_path=TEMPLATE_PATH, job=jobs[index], user_job=user_jobs[index]
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs=jobs,
            current_job_id=str(jobs[index].job_id),
            callback_prefix=button_my_jobs.callback_prefix,
            user_job=user_jobs[index],
        ),
    )


@router.callback_query(F.data.startswith(button_change_job_status.callback_prefix))
async def change_job_status_handler(callback: CallbackQuery, state: FSMContext):
    current_job: Job = await JobState.get_current_job_data(state)
    jobs: list[Job] = await JobState.get_jobs_data(state)
    user_jobs: list[UserJob] = await JobState.get_user_jobs_data(state)

    index = next((i for i, j in enumerate(jobs) if j.job_id == current_job.job_id), 0)
    user_job = toggle_user_job_status(user_jobs[index])
    user_jobs[index] = user_job
    await state.update_data(user_jobs=user_jobs)

    await callback.message.edit_text(
        render_template(
            template_path=TEMPLATE_PATH, job=current_job, user_job=user_job
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs=jobs,
            current_job_id=str(current_job.job_id),
            callback_prefix=button_my_jobs.callback_prefix,
            user_job=user_job,
        ),
    )


@router.callback_query(F.data.startswith(button_delete_job.callback_prefix))
async def delete_job_handler(callback: CallbackQuery, state: FSMContext):
    try:
        current_job = await JobState.get_current_job_data(state)
        jobs = await JobState.get_jobs_data(state)
        user_jobs = await JobState.get_user_jobs_data(state)
    except Absent as e:
        await callback.answer(str(e), show_alert=True)
        await state.clear()
        return

    index_map = {str(job.job_id): i for i, job in enumerate(jobs)}
    index = index_map.get(str(current_job.job_id), 0)

    delete_user_job(user_jobs[index])
    del jobs[index]
    del user_jobs[index]

    if not jobs:
        await callback.message.edit_text("No jobs left.")
        await state.clear()
        return

    new_index = min(index, len(jobs) - 1)
    new_job, new_user_job = jobs[new_index], user_jobs[new_index]

    await state.update_data(current_job=new_job, jobs=jobs, user_jobs=user_jobs)

    await callback.message.edit_text(
        render_template(
            template_path=TEMPLATE_PATH, job=new_job, user_job=new_user_job
        ),
        parse_mode="HTML",
        reply_markup=get_user_job_menu_keyboard(
            jobs,
            str(new_job.job_id),
            button_my_jobs.callback_prefix,
            new_user_job,
        ),
    )
