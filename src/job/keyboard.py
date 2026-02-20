import uuid
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.job.model import JobModel

# Example: list of JobModel instances
jobs: list[JobModel] = [
    JobModel(job_id=str(uuid.uuid4()), job_name="Backend Developer"),
    JobModel(job_id=str(uuid.uuid4()), job_name="Frontend Developer"),
    JobModel(job_id=str(uuid.uuid4()), job_name="Data Scientist"),
]

# Dynamically build inline keyboard
jobs_list_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=job.job_name, callback_data=f"job_{job.job_id}")]
        for job in jobs
    ]
)
