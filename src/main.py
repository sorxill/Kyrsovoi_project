"""
Основная точка запуска FastAPI приложения. (Запуска API сервера).
"""

import uvicorn
from fastapi import FastAPI

from src.api.handlers import router

testing_company = FastAPI(
    title="Testing of company",
)

testing_company.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:testing_company", reload=True)
