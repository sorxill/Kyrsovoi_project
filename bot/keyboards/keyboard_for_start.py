"""
Модуль, который добавляет кнопки в клавиатуру.
"""
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup

from bot.keyboards.keyboard_button import KeyButton

# Задаем параметр ресайза клавиатуры и создаем клавиатуру.
keyboard_for_start = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавление к клавиатуре кнопки.
keyboard_for_start.add(KeyButton.start_testing)
keyboard_for_start.add(KeyButton.create_testing)
keyboard_for_start.add(KeyButton.profile)
keyboard_for_start.add(KeyButton.contacts_with_dev)
