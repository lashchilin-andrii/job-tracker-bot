from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from src.exceptions import Absent


class BaseStatesGroup(StatesGroup):
    @staticmethod
    async def get_state_value(state: FSMContext, key: str, name: str | None = None):
        data = await state.get_data()
        value = data.get(key)
        if value is None:
            raise Absent(f"{name or key} not found in FSM state")
        return value
