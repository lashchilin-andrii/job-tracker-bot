from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.button import BUTTON_PROFILE, BUTTON_SAVED_JOBS

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BUTTON_PROFILE)],
        [KeyboardButton(text=BUTTON_SAVED_JOBS)],
    ],
    resize_keyboard=True,
)
