"""Main endpoint."""

import uvicorn
from fastapi import FastAPI


testing_company = FastAPI(
    title="Testing of company",
)


@testing_company.post("/", description="Ping APP", name="Get rout For Ping", status_code=201)
def start_answer(msg: str) -> dict:
    """Check the tests and e.t.c."""
    return {
        "args": {"up": msg.upper(), "low": msg.lower(), "base": msg.title()},
        "answer": "Success",
    }


if __name__ == "__main__":
    uvicorn.run("main:testing_company", host="0.0.0.0", reload=True, port=9000)
