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

# Startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Start
CMD ["/app/start.sh"]