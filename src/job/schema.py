from pydantic import BaseModel
from uuid import UUID


class Job(BaseModel):
    job_id: UUID
    job_name: str
    job_location: str | None = None
    job_snippet: str | None = None
    job_salary: str | None = None
    job_source: str | None = None
    job_type: str | None = None
    job_link: str | None = None
    job_company: str | None = None
    job_updated: str | None = None
