FROM python:3.10.12-alpine

WORKDIR /app

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /app

EXPOSE 9000

RUN poetry install
