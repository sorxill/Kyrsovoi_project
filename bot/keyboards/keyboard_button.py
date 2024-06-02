from aiogram import types


class KeyButton:
    start_testing = types.KeyboardButton(text="Пройти тест")
    create_testing = types.KeyboardButton(text="Создать тест")
    profile = types.KeyboardButton(text="Профиль")
    contacts_with_dev = types.KeyboardButton(text="Тех. Поддержка")
