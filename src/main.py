"""
Основная точка запуска FastAPI приложения. (Запуска API сервера).
"""

import uvicorn
from fastapi import FastAPI


testing_company = FastAPI(
    title="Testing of company",
)


@testing_company.get("/", name="Ping API", description="Test pinging API", status_code=200)
def ping_server() -> dict:
    return {
        "status_code": "200 OK"
    }


@testing_company.post("/text", description="Test working post", name="Up/Low/Title", status_code=201)
def start_answer(msg: str) -> dict:
    """Check the tests and e.t.c."""
    return {
        "args": {"up": msg.upper(), "low": msg.lower(), "base": msg.title()},
        "answer": "Success",
    }


if __name__ == "__main__":
    uvicorn.run("main:testing_company", reload=True)
