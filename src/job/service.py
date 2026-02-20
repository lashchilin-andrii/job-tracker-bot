from pathlib import Path
from jinja2 import Template
from src.job.repository import JobRepository
from src.job.model import JobModel
from src.exceptions import InvalidCallbackData


def get_all_jobs() -> list[JobModel]:
    return JobRepository().read_all()


def get_job_id_from_callback(data: str | None) -> str:
    if not data:
        raise InvalidCallbackData("Callback data is empty")

    try:
        prefix, job_id = data.split("_", 1)
    except ValueError:
        raise InvalidCallbackData("Invalid callback format")

    if prefix != "job" or not job_id:
        raise InvalidCallbackData("Invalid job callback")

    return job_id


def render_job(job: JobModel) -> str:
    template_path = Path(__file__).parent / "template" / "job.html"

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(job=job)
