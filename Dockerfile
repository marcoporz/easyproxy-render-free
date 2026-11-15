# EasyProxy Manifest-Only - Dockerfile per Render Free Tier
FROM python:3.11-slim

# Install system dependencies - MINIMAL per risparmiare RAM
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    --no-install-recommends \
    chromium \
    xvfb \
    xauth \
    netcat-openbsd \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy application files
COPY . /app/

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install FlareSolverr
RUN mkdir -p /opt/flaresolverr /opt/fsvenv && \
    git clone --depth 1 --branch v3.5.2 https://github.com/FlareSolverr/FlareSolverr.git /opt/flaresolverr && \
    python3 -m venv /opt/fsvenv && \
    /opt/fsvenv/bin/pip install --no-cache-dir -r /opt/flaresolverr/requirements.txt

# Environment variables
ENV PORT=10000
ENV FLARESOLVERR_PORT=8191
ENV FLARESOLVERR_URL=http://127.0.0.1:8191
ENV LOG_LEVEL=WARNING
ENV MANIFEST_ONLY=true
ENV DISABLE_PROXY=true
ENV DISABLE_HLS_PROXY=true
ENV DISABLE_DASH_PROXY=true
ENV DISABLE_RECORDING=true
ENV LOG_LEVEL=WARNING

# Expose port
EXPOSE 10000

# Start FlareSolverr + EasyProxy
# FlareSolverr runs on port 8191 (internal), EasyProxy on port 10000
CMD cd /opt/flaresolverr && \
    PORT=8191 HOST=127.0.0.1 LOG_LEVEL=ERROR LOG_HTML=false \
    PYTHONPATH=/opt/flaresolverr/src \
    /opt/fsvenv/bin/python -u src/flaresolverr.py & \
    sleep 5 && \
    curl -sf "http://127.0.0.1:8191/v1" >/dev/null 2>&1 && \
    echo "=== FLARESOLVERR READY ===" && \
    cd /app && \
    export PORT=10000 && \
    export FLARESOLVERR_URL="http://127.0.0.1:8191" && \
    export LOG_LEVEL=WARNING && \
    export MANIFEST_ONLY=true && \
    export DISABLE_PROXY=true && \
    export DISABLE_HLS_PROXY=true && \
    export DISABLE_DASH_PROXY=true && \
    export DISABLE_RECORDING=true && \
    exec python3 main.py