FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

WORKDIR /app/src

EXPOSE 8000

RUN pip install --no-cache-dir poetry