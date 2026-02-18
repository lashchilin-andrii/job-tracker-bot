from pydantic import BaseModel
from uuid import UUID


class Job(BaseModel):
    job_id: UUID
    job_name: str
