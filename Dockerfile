FROM python:3.11-slim

# Update package lists and install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    make g++ && rm -rf /var/lib/apt/lists/*

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.2

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . /app

EXPOSE 8080

ENTRYPOINT ["poetry", "run","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]