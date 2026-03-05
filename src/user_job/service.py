from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.job.model import JobModel
from src.job.service import render_job
from src.job.keyboard import get_menu_keyboard
from src.job.repository import JobRepository
from src.user_job.model import UserJobModel
from src.user_job.repository import UserJobRepository
from src.button import button_my_jobs
from src.job.state import CurrentJobState
from src.job.message import (
    MSG_NOT_FOUND,
)


async def save_job(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    job_data = data.get("job")

    if not job_data:
        await callback.message.answer("❌ No job in state")
        return
    print(job_data)

    job = JobModel(**job_data.model_dump())

    existing = JobRepository().read_by_property("job_id", job.job_id)
    if not existing:
        JobRepository().create_one(job)

    user_job = UserJobModel(
        user_id=callback.from_user.id,
        job_id=job.job_id,
        user_job_status="Applied",
    )

    UserJobRepository().create_one(user_job)

    await callback.message.answer("✅ Job saved successfully")


async def show_my_jobs(message: Message, state: FSMContext):
    user_jobs = UserJobRepository().read_by_property(
        "user_id", message.from_user.id, read_all=True
    )
    if not user_jobs:
        await message.answer(MSG_NOT_FOUND)
        return

    jobs = [
        job
        for uj in user_jobs
        if (job := JobRepository().read_by_property("job_id", uj.job_id))
    ]

    if not jobs:
        await message.answer(MSG_NOT_FOUND)
        return

    # сохраняем первый job и индекс в FSM
    await state.set_state(CurrentJobState.job)
    await state.update_data(job=jobs[0], user_jobs=jobs)

    await message.answer(
        render_job(jobs[0]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            jobs=jobs,
            callback_prefix=button_my_jobs.callback_prefix,
        ),
    )


async def handle_my_jobs_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    jobs = data.get("user_jobs")
    if not jobs:
        await callback.message.answer(MSG_NOT_FOUND)
        return

    # получаем текущий индекс из callback или из FSM
    job_id = button_my_jobs.get_data_from_callback_without_prefix(callback.data)
    index = next((i for i, job in enumerate(jobs) if str(job.job_id) == job_id), 0)

    # обновляем FSM
    await state.update_data(job=jobs[index])

    await callback.message.edit_text(
        render_job(jobs[index]),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            current_job_index=index,
            jobs=jobs,
            callback_prefix=button_my_jobs.callback_prefix,
        ),
    )
