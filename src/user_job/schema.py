from pydantic import BaseModel

from src.base.enum import UserJobStatus


class UserJob(BaseModel):
    user_id: str
    job_id: str
    user_job_status: str = UserJobStatus.applied.value
