"""
Модуль, отвечающий за получение секретных данных, из переменных окружения.
"""

import os

from dotenv import load_dotenv

# Загружаем окружение.
load_dotenv()

# Из объекта environ(окружение) получаем данные переменных.
DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
TG_TOKEN = os.environ["TG_TOKEN"]
