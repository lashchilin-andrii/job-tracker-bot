from pydantic import BaseModel


class JoobleJob(BaseModel):
    job_title: str
    job_location: str
    job_snippet: str
    job_salary: str
    job_source: str
    job_type: str
    job_link: str
    job_company: str
    job_updated: str
    job_id: int
