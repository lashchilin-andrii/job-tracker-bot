from collections import Counter


from src.user_job.schema import UserJobStats
from src.exceptions import Absent, Present
from src.user_job.schema import UserJob
from src.user_job.model import UserJobModel
from src.user_job.repository import UserJobRepository
from src.base.enum import UserJobStatus
from sqlalchemy.exc import IntegrityError


async def save_my_job(user_job: UserJob) -> UserJobModel:
    """Save user_job or raise exception."""
    try:
        return UserJobRepository().create_one(
            UserJobModel(
                user_id=user_job.user_id,
                job_id=user_job.job_id,
                user_job_status=UserJobStatus.applied.value,
            )
        )
    except IntegrityError:
        raise Present


def get_all_user_jobs_by_user_id(user_id: int | str) -> list[UserJobModel]:
    """Get all user_jobs objects by user_id."""
    user_jobs = UserJobRepository().read_all_by_property("user_id", str(user_id))

    if not user_jobs:
        raise Absent("You have not saved any jobs yet.")

    return user_jobs


def toggle_user_job_status(user_job: UserJob) -> UserJob:
    """Change job status of given object in db."""
    statuses = list(UserJobStatus)

    try:
        current_idx = next(
            i for i, s in enumerate(statuses) if s.value == user_job.user_job_status
        )
    except StopIteration:
        current_idx = 0

    new_status = statuses[(current_idx + 1) % len(statuses)].value
    user_job.user_job_status = new_status

    user_job_model = UserJobModel(
        user_id=user_job.user_id,
        job_id=user_job.job_id,
        user_job_status=user_job.user_job_status,
    )

    UserJobRepository().update_one(user_job_model)

    return user_job


def delete_user_job(user_job: UserJob) -> None:
    """Delete a user_job by converting Pydantic model to SQLAlchemy model. Raises Absent if the object does not exist in DB."""
    db_obj = UserJobRepository().get_from_pydantic(user_job)
    if not db_obj:
        raise Absent("User job not found in database")
    UserJobRepository().delete_one(db_obj)


def get_user_job_stats(user_id: str) -> UserJobStats:
    user_jobs = UserJobRepository().read_all_by_property("user_id", user_id) or []

    counter = Counter(uj.user_job_status for uj in user_jobs)

    data = {status.name: counter.get(status.value, 0) for status in UserJobStatus}

    data["total"] = len(user_jobs)

    return UserJobStats(**data)
