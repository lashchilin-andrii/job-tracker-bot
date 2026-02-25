from aiogram.fsm.state import StatesGroup, State


class GetAJobState(StatesGroup):
    keywords = State()
    location = State()
