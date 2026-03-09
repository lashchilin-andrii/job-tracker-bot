from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.job.schema import Job


class JobSearchParametersState(StatesGroup):
    keywords = State()
    location = State()

    @staticmethod
    async def get_keywords(state: FSMContext) -> str | None:
        """Get the 'keywords' value from FSM state."""
        data = await state.get_data()
        return data.get("keywords")

    @staticmethod
    async def get_location(state: FSMContext) -> str | None:
        """Get the 'location' value from FSM state."""
        data = await state.get_data()
        return data.get("location")


class CurrentJobState(StatesGroup):
    job = State()

    @staticmethod
    async def get_job_data(state: FSMContext) -> Job | None:
        """Get the 'job' object from FSM state."""
        data = await state.get_data()
        return data.get("job")
