# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# System dependencies for OpenCV/Ultralytics and building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir "poetry==1.8.3"

# Copy lockfiles first to leverage Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install Python dependencies (no dev deps). Poetry installs to the global env due to POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --only main --no-ansi

# Copy the application code and model weights
COPY python_fast_api ./python_fast_api
wget -P "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n-pose.pt" ./

# Cloud Run expects the service to listen on $PORT; default to 8080
ENV PORT=8080
EXPOSE 8080

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "python_fast_api.main:app", "--host", "0.0.0.0", "--port", "8080"]


