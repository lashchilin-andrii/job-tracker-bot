from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.button import BUTTON_GET_A_JOB, BUTTON_PROFILE, BUTTON_SAVED_JOBS

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BUTTON_PROFILE)],
        [KeyboardButton(text=BUTTON_SAVED_JOBS)],
        [KeyboardButton(text=BUTTON_GET_A_JOB)],
    ],
    resize_keyboard=True,
)
