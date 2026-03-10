from sqlalchemy.exc import IntegrityError

from src.job.repository import JobRepository
from src.job.schema import Job
from src.job.model import JobModel
from src.exceptions import Absent


async def save_job(job: Job | None) -> Job:
    """Save job if not exists."""
    if not job:
        raise Absent("No job in save_job")
    job_model = JobModel(**job.model_dump())

    try:
        return Job.model_validate(JobRepository().create_one(job_model).__dict__)
    except IntegrityError:
        return Job.model_validate(
            JobRepository().read_one_by_property("job_id", job_model.job_id).__dict__
        )


def get_jobs_by_ids(job_ids: list[str]) -> list[Job]:
    """Get list of Job object from db by their ids."""
    jobs = [
        Job.model_validate(job.__dict__)
        for job_id in job_ids
        if (job := JobRepository().read_one_by_property("job_id", job_id))
    ]
    if not jobs:
        raise Absent("No jobs found for provided job IDs.")
    return jobs
