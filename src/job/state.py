from aiogram.fsm.state import StatesGroup, State


class JobSearchParametersState(StatesGroup):
    keywords = State()
    location = State()


class CurrentJobState(StatesGroup):
    job = State()
