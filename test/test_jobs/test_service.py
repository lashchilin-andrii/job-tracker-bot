from unittest.mock import patch, MagicMock

from src.job.service import (
    get_saved_jobs,
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

    jobs = get_saved_jobs()

    assert len(jobs) == 2
    assert jobs[0].job_name == "Backend"
    mock_repo.read_all.assert_called_once()
