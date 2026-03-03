from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.job.model import JobModel
from src.job.repository import JobRepository
from src.user_job.model import UserJobModel
from src.user_job.repository import UserJobRepository


async def save_job(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    job_data = data.get("job")

    if not job_data:
        await callback.message.answer("❌ No job in state")
        return

    job = JobModel(**job_data)

    existing = JobRepository().read_one_by_property("job_id", job.job_id)
    if not existing:
        JobRepository().create_one(job)

    user_job = UserJobModel(
        user_id=callback.from_user.id,
        job_id=job.job_id,
        user_job_status="Applied",
    )

    UserJobRepository().create_one(user_job)

    await callback.message.answer("✅ Job saved successfully")
