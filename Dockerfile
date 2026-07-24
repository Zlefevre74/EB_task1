FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install --no-root

WORKDIR /app/src
CMD ["poetry", "run", "uvicorn",
  "application:get_app", "--host", "0.0.0.0",
  "--port", "8000", "--factory"]