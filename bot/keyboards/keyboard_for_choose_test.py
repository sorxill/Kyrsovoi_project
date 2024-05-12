from aiogram.types.reply_keyboard import ReplyKeyboardMarkup

from .keyboard_button import KeyButton

choose_test_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

choose_test_keyboard.add(KeyButton.yes)
choose_test_keyboard.add(KeyButton.no)
