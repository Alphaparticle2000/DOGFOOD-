# ==============================================================================
# DOGFOOD Backend — FastAPI (production image)
#
# Runs as a non-root user and binds to the platform-assigned $PORT so the same
# image works locally, under Docker Compose, and on Render.
# docker-compose.yml overrides CMD with --reload for local development.
# ==============================================================================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# curl backs the Docker HEALTHCHECK below.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencies are copied alone first so this layer caches across source edits.
COPY backend/requirements.txt /app/requirements.txt
# --retries/--timeout so a slow or flaky registry does not fail the whole build.
RUN pip install --no-cache-dir --retries 5 --timeout 120 \
    -r /app/requirements.txt

# Application source. The package is imported as backend.app.* (PYTHONPATH=/app).
COPY backend/ /app/backend/
COPY fixtures.json /app/fixtures.json

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f "http://127.0.0.1:${PORT:-8000}/health" || exit 1

# Render injects PORT; fall back to 8000 for local runs.
CMD ["sh", "-c", "exec uvicorn backend.app.main:app --host 0.0.0.0 --port \"${PORT:-8000}\""]
