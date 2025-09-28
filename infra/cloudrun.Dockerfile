FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY server/requirements.txt ./server/requirements.txt
RUN python -m venv /venv && /venv/bin/pip install -r server/requirements.txt

COPY server ./server
ENV PATH="/venv/bin:$PATH"
EXPOSE 8080

# uvicorn with workers=1 is typical for SSE to keep ordering simple.
CMD ["uvicorn", "server.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
