from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


jobs_list_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Job 1", callback_data="job_1")],
        [InlineKeyboardButton(text="Job 2", callback_data="job_2")],
        [InlineKeyboardButton(text="Job 3", callback_data="job_3")],
    ]
)
