# syntax=docker/dockerfile:1.3

# Base image
FROM python:3.13-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.1 \
    POETRY_HOME="/root/.local" \
    PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH="/event_system"

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl libpq-dev && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 - && \
    /root/.local/bin/poetry --version

# Set work directory
WORKDIR /event_system

# Copy project files
COPY . .

# Install project dependencies
RUN /root/.local/bin/poetry install

# Development stage for consumer
FROM base as consumer
CMD ["/root/.local/bin/poetry", "run", "uvicorn", "event_system.services.event_consumer.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Development stage for propagator
FROM base as propagator
CMD ["/root/.local/bin/poetry", "run", "python", "-m", "event_system.services.event_propagator.main"]