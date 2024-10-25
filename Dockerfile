# Using a base image with Python
FROM python:3.9-slim

# Installing system dependencies required for building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Installing Poetry
RUN pip install --no-cache-dir poetry

# Setting the working directory
WORKDIR /app

# Copying project files (only configuration files)
COPY pyproject.toml poetry.lock ./

# Installing dependencies using Poetry
RUN poetry install --only main --no-interaction --no-ansi

# Copying remaining project files
COPY . .

ENV PYTHONPATH "/app"

# Command to run FastAPI using Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
