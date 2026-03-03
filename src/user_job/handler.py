from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.button import button_save_job
from src.user_job.service import save_job

router = Router()


@router.callback_query(F.data.startswith(button_save_job.callback_prefix))
async def save_job_handler(callback: CallbackQuery, state: FSMContext):
    await save_job(callback, state)
