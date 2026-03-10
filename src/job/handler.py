from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.message import MSG_ENTER_KEYWORDS, MSG_ENTER_LOCATION
from src.button import button_browse_jobs
from src.job.service import (
    handle_browse_jobs_callback,
    process_location_step,
)
from src.state import JobSearchParametersState

router = Router()


@router.callback_query(F.data.startswith(button_browse_jobs.callback_prefix))
async def browse_jobs_callback_handler(callback: CallbackQuery, state: FSMContext):
    await handle_browse_jobs_callback(callback, state)


@router.message(F.text == button_browse_jobs.text)
async def browse_jobs_handler(message: Message, state: FSMContext):
    await state.set_state(JobSearchParametersState.keywords)
    await message.answer(MSG_ENTER_KEYWORDS)


@router.message(JobSearchParametersState.keywords)
async def process_keywords(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await state.set_state(JobSearchParametersState.location)
    await message.answer(MSG_ENTER_LOCATION)


@router.message(JobSearchParametersState.location)
async def process_location(message: Message, state: FSMContext):
    await process_location_step(message, state)
