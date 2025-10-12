# Dockerfile for OdeaDev-AI-TTS
# Compatible with Render, RunPod, and other Docker platforms

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY .env.example .env

# Create directory for database
RUN mkdir -p /data

# Environment variables (override with -e or docker-compose)
ENV DATABASE_URL=sqlite:////data/odeadev_tts.db
ENV PORT=8000
ENV HOST=0.0.0.0
ENV ENFORCE_AUTH=true
ENV PYTHONUNBUFFERED=1

# Expose port (Render will override with $PORT)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Initialize database on first run, then start server
# Use $PORT for Render compatibility (they inject it)
CMD python -m src.init_db && \
    uvicorn src.main:app --host ${HOST} --port ${PORT:-8000}
