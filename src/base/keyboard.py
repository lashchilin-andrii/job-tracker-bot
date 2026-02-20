from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.button import BUTTON_PROFILE, BUTTON_JOBS

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BUTTON_PROFILE)],
        [KeyboardButton(text=BUTTON_JOBS)],
    ],
    resize_keyboard=True,
)
