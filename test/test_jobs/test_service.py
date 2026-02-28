import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from src.job.service import (
    get_my_jobs,
    get_job_id_from_callback,
    find_job_index,
    show_my_jobs,
    handle_my_jobs_callback,
    handle_browse_jobs_callback,
    process_keywords_step,
    process_location_step,
)
from src.job.model import JobModel
from src.button import button_browse_jobs
from src.exceptions import InvalidCallbackData
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


# -----------------------
# Synchronous tests
# -----------------------


def test_get_job_id_from_callback_valid():
    data = "job_12345"
    result = get_job_id_from_callback(data)
    assert result == "12345"


def test_get_job_id_from_callback_invalid_empty():
    with pytest.raises(InvalidCallbackData):
        get_job_id_from_callback(button_browse_jobs.callback)


def test_get_job_id_from_callback_invalid_none():
    with pytest.raises(InvalidCallbackData):
        get_job_id_from_callback(None)


@patch("src.job.service.JobRepository")
def test_get_my_jobs(mock_repo_class):
    mock_repo = MagicMock()
    mock_repo.read_all.return_value = [
        JobModel(job_id="1", job_name="Backend"),
        JobModel(job_id="2", job_name="Frontend"),
    ]
    mock_repo_class.return_value = mock_repo

    jobs = get_my_jobs()

    assert len(jobs) == 2
    assert jobs[0].job_name == "Backend"
    mock_repo.read_all.assert_called_once()


def test_find_job_index():
    jobs = [
        JobModel(job_id="1", job_name="Backend"),
        JobModel(job_id="2", job_name="Frontend"),
    ]
    idx = find_job_index(jobs, "2")
    assert idx == 1

    with pytest.raises(InvalidCallbackData):
        find_job_index(jobs, "3")


# -----------------------
# Asynchronous tests
# -----------------------
@pytest.mark.asyncio
async def test_show_my_jobs(monkeypatch):
    fake_message = MagicMock(spec=Message)
    fake_message.answer = AsyncMock()

    fake_jobs = [JobModel(job_id="1", job_name="Backend")]
    monkeypatch.setattr("src.job.service.get_my_jobs", lambda: fake_jobs)

    await show_my_jobs(fake_message)
    fake_message.answer.assert_called()


@pytest.mark.asyncio
async def test_handle_my_job_callback(monkeypatch):
    fake_message = MagicMock()
    fake_message.answer = AsyncMock()
    fake_message.edit_text = AsyncMock()

    fake_callback = MagicMock()
    fake_callback.data = "my_job_1"
    fake_callback.message = fake_message
    fake_callback.answer = AsyncMock()

    fake_jobs = [JobModel(job_id="1", job_name="Backend")]
    monkeypatch.setattr("src.job.service.get_my_jobs", lambda: fake_jobs)

    await handle_my_jobs_callback(fake_callback)
    fake_message.edit_text.assert_called()


@pytest.mark.asyncio
async def test_handle_found_job_callback(monkeypatch):

    # Мок для message
    fake_message = MagicMock()
    fake_message.answer = AsyncMock()
    fake_message.edit_text = AsyncMock()

    # Мок для callback
    fake_callback = MagicMock()
    fake_callback.data = "job_1"
    fake_callback.message = fake_message  # важно!
    fake_callback.answer = AsyncMock()

    fake_jobs = [JobModel(job_id="1", job_name="Backend")]

    monkeypatch.setattr("src.job.service.get_job_id_from_callback", lambda data: "1")
    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={"found_jobs": fake_jobs})

    fake_callback.data = "job_1"

    await handle_browse_jobs_callback(fake_callback, state)
    fake_message.edit_text.assert_called_once()


@pytest.mark.asyncio
async def test_process_keywords_step():
    fake_message = MagicMock(spec=Message)
    fake_message.answer = AsyncMock()
    state = MagicMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    fake_message.text = "python backend"
    await process_keywords_step(fake_message, state)

    state.update_data.assert_called_once()
    state.set_state.assert_called_once()
    fake_message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_process_location_step(monkeypatch):
    fake_message = MagicMock(spec=Message)
    fake_message.answer = AsyncMock()
    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={"keywords": "python backend"})
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    fake_message.text = "Remote"

    # мок для get_jobs
    monkeypatch.setattr(
        "src.job.service.get_jobs",
        lambda keywords, location: [JobModel(job_id="1", job_name="Backend")],
    )

    monkeypatch.setattr(
        "src.job.service.render_job", lambda job: f"Job: {job.job_name}"
    )
    monkeypatch.setattr(
        "src.job.service.get_menu_keyboard", lambda index, jobs, prefix: "keyboard"
    )

    await process_location_step(fake_message, state)
    fake_message.answer.assert_called()
    state.update_data.assert_called()
    state.set_state.assert_called()
