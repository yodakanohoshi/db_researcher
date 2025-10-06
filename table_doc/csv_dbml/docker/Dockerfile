# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# uv導入
RUN apt update &&apt install -y --no-install-recommends curl ca-certificates
RUN rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN ln -s /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN uv venv --seed && uv sync --no-dev
ENV PATH="/app/.venv/bin:${PATH}"

WORKDIR /sandbox
# 動作確認コマンド
CMD ["bash"]