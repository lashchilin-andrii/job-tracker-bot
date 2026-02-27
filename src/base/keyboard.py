from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.button import button_browse_jobs, button_profile, button_my_jobs

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=button_profile.text)],
        [KeyboardButton(text=button_my_jobs.text)],
        [KeyboardButton(text=button_browse_jobs.text)],
    ],
    resize_keyboard=True,
)
