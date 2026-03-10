from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from src.exceptions import Absent
from src.job.schema import Job
from src.user_job.schema import UserJob


class BaseStatesGroup(StatesGroup):
    @staticmethod
    async def get_state_value(state: FSMContext, key: str, name: str | None = None):
        data = await state.get_data()
        value = data.get(key)
        if value is None:
            raise Absent(f"{name or key} not found in FSM state")
        return value


class JobSearchParametersState(BaseStatesGroup):
    keywords = State()
    location = State()

    @staticmethod
    async def get_keywords(state: FSMContext) -> str:
        return await BaseStatesGroup.get_state_value(state, "keywords", "keywords")

    @staticmethod
    async def get_location(state: FSMContext) -> str:
        return await BaseStatesGroup.get_state_value(state, "location", "location")


class JobState(BaseStatesGroup):
    current_job = State()
    found_jobs = State()
    user_jobs = State()
    jobs = State()

    @staticmethod
    async def get_current_job_data(state: FSMContext) -> Job:
        return await BaseStatesGroup.get_state_value(
            state, "current_job", "current_job"
        )

    @staticmethod
    async def get_found_jobs_data(state: FSMContext) -> list[Job]:
        return await BaseStatesGroup.get_state_value(state, "found_jobs", "found_jobs")

    @staticmethod
    async def get_user_jobs_data(state: FSMContext) -> list[UserJob]:
        return await BaseStatesGroup.get_state_value(state, "user_jobs", "user_jobs")

    @staticmethod
    async def get_jobs_data(state: FSMContext) -> list[Job]:
        return await BaseStatesGroup.get_state_value(state, "jobs", "jobs")
