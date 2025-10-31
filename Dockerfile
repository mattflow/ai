FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.9.6 /uv /uvx /bin/
RUN apt-get update && apt-get install -y curl

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN uv sync --locked

COPY app app