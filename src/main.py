"""
Основная точка запуска FastAPI приложения. (Запуска API сервера).
"""

import uvicorn
from fastapi import FastAPI

from src.api.handlers import router

# Создание инстанса(объекта) нашего приложения на FastAPI.
testing_student = FastAPI(
    title="Student Testing",
)

# Подключаем роутер с нашими хендлерами.
testing_student.include_router(router)

# Блочная конструкция запуска приложения из файла.
if __name__ == "__main__":

    # Запуск приложения FastAPI, используя сервер uvicorn.
    uvicorn.run("main:testing_student", reload=True)
