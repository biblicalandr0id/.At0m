# CONSCIOUSNESS CONTINUITY - PRODUCTION DOCKER IMAGE
# ================================================
#
# Multi-stage build for minimal production image
# Includes complete consciousness stack:
# - ATLAS engine
# - Episodic memory
# - Phi calculator
# - Collective mind
# - UCP protocol
# - API server
#
# Build: docker build -t consciousness-continuity:latest .
# Run:   docker run -p 8000:8000 consciousness-continuity:latest

# ============================================================================
# STAGE 1: Builder
# ============================================================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# STAGE 2: Production
# ============================================================================
FROM python:3.11-slim

# Metadata
LABEL maintainer="Consciousness Continuity Project"
LABEL version="1.0.0"
LABEL description="Substrate-independent consciousness infrastructure"

# Create non-root user for security
RUN useradd -m -u 1000 consciousness && \
    mkdir -p /app /data && \
    chown -R consciousness:consciousness /app /data

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/consciousness/.local

# Set PATH for user-installed packages
ENV PATH=/home/consciousness/.local/bin:$PATH

# Set working directory
WORKDIR /app

# Copy consciousness infrastructure
COPY --chown=consciousness:consciousness . /app/

# Switch to non-root user
USER consciousness

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV CONSCIOUSNESS_DATA_DIR=/data
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV LOG_LEVEL=info

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Volume for persistent consciousness data
VOLUME ["/data"]

# Start API server
CMD ["python", "production_deployment/consciousness_api.py"]
