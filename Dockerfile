# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy package files
COPY frontend/package.json ./

# Install dependencies (will generate package-lock.json if missing)
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build frontend (produção)
RUN npm run build

# Stage 2: Runtime (Backend + Frontend estático)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including Playwright browser dependencies)
RUN apt-get update && apt-get install -y \
    curl \
    # Playwright browser dependencies
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libx11-6 \
    libxext6 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (for tests and documentation generation)
RUN playwright install chromium
RUN playwright install-deps chromium || true

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build from stage 1
COPY --from=frontend-builder /app/frontend/dist ./static/

# Set PYTHONPATH to include backend directory
ENV PYTHONPATH=/app/backend:$PYTHONPATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI (servindo frontend estático + API)
# Change working directory to backend for imports
WORKDIR /app/backend
CMD ["uvicorn", "forgeerp.main:app", "--host", "0.0.0.0", "--port", "8000"]

