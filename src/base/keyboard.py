from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.button import button_browse_jobs, button_profile, button_my_jobs
from aiogram.types import InlineKeyboardButton
from src.base.button import ButtonBase

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=button_profile.text)],
        [KeyboardButton(text=button_my_jobs.text)],
        [KeyboardButton(text=button_browse_jobs.text)],
    ],
    resize_keyboard=True,
)


def get_keyboard_with_buttons(
    include_buttons: list[list[ButtonBase]],
) -> list[list[InlineKeyboardButton]]:

    keyboard: list[list[InlineKeyboardButton]] = []

    for row in include_buttons:
        keyboard_row: list[InlineKeyboardButton] = []

        for button in row:
            keyboard_row.append(
                InlineKeyboardButton(
                    text=button.text,
                    callback_data=button.callback_prefix,
                )
            )

        keyboard.append(keyboard_row)

    return keyboard
