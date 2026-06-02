FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml ./

RUN uv sync --no-dev --no-root

RUN uv add gunicorn

COPY . .

EXPOSE 5000

CMD ["/app/.venv/bin/gunicorn", "--bind", "0.0.0.0:5000", "main:create_app()"]