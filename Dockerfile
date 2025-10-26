FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install gcc libpq-dev python3-dev -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.1

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction

COPY . .

