# builder
FROM python:3.12 as builder

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root && rm -rf $POETRY_CACHE_DIR

# runtime
FROM builder as runtime

RUN useradd --create-home appuser

WORKDIR /app

USER appuser
COPY --from=builder /app/.venv ./.venv

COPY --chown=appuser:appuser astrotoolz_api ./astrotoolz_api

ENTRYPOINT ["uvicorn"]
CMD ["astrotoolz_api.main:app", "--host", "0.0.0.0", "--port", "8002", "--log-config", "astrotoolz_api/logger_conf.yaml"]
