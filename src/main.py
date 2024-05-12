"""Main endpoint."""

import uvicorn
from fastapi import FastAPI


testing_company = FastAPI(
    title="Testing of company",
)


@testing_company.get("/", description="Ping APP", name="Get rout For Ping")
def start_answer() -> dict:
    """Check the tests and e.t.c."""
    return {
        "answer": "Success",
    }


if __name__ == "__main__":
    uvicorn.run("main:testing_company", host="0.0.0.0", reload=True, port=9000)
