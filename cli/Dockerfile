FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml
COPY pyproject.toml .

# Install CLI
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Default command
CMD ["forge", "--help"]

