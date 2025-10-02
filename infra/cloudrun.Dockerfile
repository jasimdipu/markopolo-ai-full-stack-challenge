FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set workdir where your FastAPI package lives
WORKDIR /app/server

# Install deps
COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install -r requirements.txt

# Copy the rtcrm
COPY server/ .

ENV PATH="/venv/bin:$PATH"
EXPOSE 8080

# With WORKDIR=/rtcrm/server, rtcrm.main:rtcrm resolves correctly
CMD ["uvicorn", "rtcrm.main:app", "--host", "0.0.0.0", "--port", "8080"]
