# Use the official Python lightweight image
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# Copy local code to the container image
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install production dependencies
RUN pip install --no-cache-dir .

# Hardening: Run as non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Run the web service on container startup.
CMD exec uvicorn verdaterrakai.app.main:app --host 0.0.0.0 --port ${PORT} --workers 1
