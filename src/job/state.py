from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.exceptions import Absent
from src.job.schema import Job


class JobSearchParametersState(StatesGroup):
    keywords = State()
    location = State()

    @staticmethod
    async def get_keywords(state: FSMContext) -> str:
        data = await state.get_data()
        keywords = data.get("keywords")

        if not keywords:
            raise Absent("keywords not found in FSM state")

        return keywords

    @staticmethod
    async def get_location(state: FSMContext) -> str:
        data = await state.get_data()
        location = data.get("location")

        if not location:
            raise Absent("location not found in FSM state")

        return location


class CurrentJobState(StatesGroup):
    job = State()

    @staticmethod
    async def get_job_data(state: FSMContext) -> Job:
        data = await state.get_data()
        job = data.get("job")

        if not job:
            raise Absent("job not found in FSM state")

        return job
