FROM python:3.11-slim
WORKDIR /app
RUN useradd -m app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY --chown=app:app src ./src
EXPOSE 8000

# Setup an app user so the container doesn't run as the root user
USER app

# Default command (used if not overridden by docker-compose or render)
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
