from pydantic import BaseModel

from src.base.enum import UserJobStatus


class UserJob(BaseModel):
    user_id: str
    job_id: str
    user_job_status: str = UserJobStatus.applied.value


class UserJobStats(BaseModel):
    applied: int = 0
    accepted: int = 0
    rejected: int = 0
    total: int = 0
