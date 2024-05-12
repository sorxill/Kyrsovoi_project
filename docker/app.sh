#!/bin/busybox

poetry run alembic upgrade head

poetry run uvicorn --reload src.main:testing_company --host=0.0.0.0 --port=9000