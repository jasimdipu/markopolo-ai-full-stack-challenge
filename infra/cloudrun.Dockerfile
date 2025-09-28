# 1. Use a specific version for reproducibility
FROM python:3.11.5-slim-bullseye as base

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3. Set the working directory
WORKDIR /app

# 4. Copy only the requirements file first to leverage Docker cache
# This assumes your requirements.txt is inside the 'server' folder
COPY server/requirements.txt .

# 5. Install dependencies (without a virtual environment, which is redundant in Docker)
RUN pip install -r requirements.txt

# 6. Create a non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app

# 7. Copy the rest of your application code
# This copies the contents of the 'server' directory into '/app'
COPY server/ .

# 8. Switch to the non-root user
USER app

# 9. Expose the port
EXPOSE 8080

# 10. Define the command to run the application
# The path changes because we copied the contents of 'server' into the root
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]