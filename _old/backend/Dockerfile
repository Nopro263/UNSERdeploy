# syntax=docker/dockerfile:1.7-labs

FROM python:3.12-bookworm

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


ENTRYPOINT [ "fastapi", "dev", "main.py",  "--host", "0.0.0.0", "--root-path", "/api" ]