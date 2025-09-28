FROM python:3.11.5-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# copy into /app so pip finds it
COPY requirements.txt ./ 
RUN pip install -r requirements.txt

RUN addgroup --system app && adduser --system --ingroup app app
COPY server/ .    # see note #3 below
USER app
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
