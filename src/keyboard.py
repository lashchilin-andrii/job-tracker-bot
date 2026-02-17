from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.button import BUTTON_PROFILE, BUTTON_VACANCIES

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BUTTON_PROFILE)],
        [KeyboardButton(text=BUTTON_VACANCIES)],
    ],
    resize_keyboard=True,
)
