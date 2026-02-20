from src.job.repository import JobRepository
from src.job.model import JobModel


def get_all_jobs() -> list[JobModel]:
    return JobRepository().read_all()


def get_job_by_id(job_id: str) -> JobModel | None:
    return JobRepository().read_one_by_property(
        property_name="job_id", property_value=job_id
    )


def get_job_id_from_callback(data: str) -> str:
    return data.split("_")[1]
