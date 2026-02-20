from unittest.mock import patch, MagicMock

from src.job.service import (
    get_all_jobs,
    get_job_by_id,
    get_job_id_from_callback,
)
from src.job.model import JobModel


def test_get_job_id_from_callback():
    data = "job_12345"
    result = get_job_id_from_callback(data)
    assert result == "12345"


@patch("src.job.service.JobRepository")
def test_get_all_jobs(mock_repo_class):
    mock_repo = MagicMock()
    mock_repo.read_all.return_value = [
        JobModel(job_id="1", job_name="Backend"),
        JobModel(job_id="2", job_name="Frontend"),
    ]
    mock_repo_class.return_value = mock_repo

    jobs = get_all_jobs()

    assert len(jobs) == 2
    assert jobs[0].job_name == "Backend"
    mock_repo.read_all.assert_called_once()


@patch("src.job.service.JobRepository")
def test_get_job_by_id(mock_repo_class):
    mock_repo = MagicMock()

    mock_repo.read_one_by_property.return_value = JobModel(
        job_id="1", job_name="Backend Developer"
    )

    mock_repo_class.return_value = mock_repo

    job = get_job_by_id("1")

    assert job is not None
    assert job.job_name == "Backend Developer"
    mock_repo.read_one_by_property.assert_called_once_with(
        property_name="job_id", property_value="1"
    )
