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
