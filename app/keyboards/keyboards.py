
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup




start_button_1 = KeyboardButton(text='* Начать Игру *')

keyboard_after_cancel = ReplyKeyboardMarkup(
    keyboard=[[start_button_1]],
    resize_keyboard=True)