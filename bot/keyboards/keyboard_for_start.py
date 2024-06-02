from aiogram.types.reply_keyboard import ReplyKeyboardMarkup

from bot.keyboards.keyboard_button import KeyButton

keyboard_for_start = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_for_start.add(KeyButton.start_testing)
keyboard_for_start.add(KeyButton.create_testing)
keyboard_for_start.add(KeyButton.profile)
keyboard_for_start.add(KeyButton.contacts_with_dev)
