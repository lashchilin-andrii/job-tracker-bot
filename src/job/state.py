from aiogram.fsm.state import StatesGroup, State


class JobState(StatesGroup):
    keywords = State()
    location = State()
