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

# Install FlareSolverr (for Cloudflare scraping)
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
ENV FLARESOLVERR_ENABLED=true

# Expose port
EXPOSE 10000

# Create startup script - EasyProxy FIRST, FlareSolverr in background
RUN echo '#!/bin/bash\nset -e\n\necho "=== Starting EasyProxy Manifest-Only on port 10000 ==="\ncd /app\nexport PORT=10000\nexport FLARESOLVERR_URL="http://127.0.0.1:8191"\nexport LOG_LEVEL=WARNING\nexport MANIFEST_ONLY=true\nexport DISABLE_PROXY=true\nexport DISABLE_HLS_PROXY=true\nexport DISABLE_DASH_PROXY=true\nexport DISABLE_RECORDING=true\nexport FLARESOLVERR_ENABLED=true\n\n# Start EasyProxy in background FIRST (health check must pass immediately)\necho "Starting EasyProxy..."\npython3 main.py > /tmp/easyproxy.log 2>&1 &\nEASYPROXY_PID=$!\n\necho "EasyProxy PID: $EASYPROXY_PID"\nsleep 2\n\n# Verify EasyProxy is responding on port 10000\nfor i in {1..15}; do\n    if curl -sf "http://127.0.0.1:10000/health" >/dev/null 2>&1; then\n        echo "=== EASYPROXY READY on port 10000 ==="\n        break\n    fi\n    if ! kill -0 $EASYPROXY_PID 2>/dev/null; then\n        echo "ERROR: EasyProxy process died"\n        cat /tmp/easyproxy.log\n        exit 1\n    fi\n    sleep 1\ndone\n\nif ! curl -sf "http://127.0.0.1:10000/health" >/dev/null 2>&1; then\n    echo "ERROR: EasyProxy health check failed after 15s"\n    cat /tmp/easyproxy.log\n    exit 1\nfi\n\n# NOW start FlareSolverr in background (non-blocking, optional)\necho "=== Starting FlareSolverr on port 8191 (background) ==="\nrm -f /tmp/.X99-lock\nXvfb :99 -screen 0 1024x768x24 > /tmp/xvfb.log 2>&1 &\nXVFB_PID=$!\nexport DISPLAY=:99\nsleep 3\n\nif ! kill -0 $XVFB_PID 2>/dev/null; then\n    echo "WARNING: Xvfb failed to start, FlareSolverr may not work"\nelse\n    echo "Xvfb running (PID: $XVFB_PID)"\n    cd /opt/flaresolverr\n    PORT=8191 HOST=127.0.0.1 LOG_LEVEL=ERROR LOG_HTML=false \\\n    PYTHONPATH=/opt/flaresolverr/src \\\n    /opt/fsvenv/bin/python -u src/flaresolverr.py > /tmp/flaresolverr.log 2>&1 &\n    FLARESOLVERR_PID=$!\n    echo "FlareSolverr started in background (PID: $FLARESOLVERR_PID)"\nfi\n\n# Wait for EasyProxy (main process)\nwait $EASYPROXY_PID' > /start.sh && chmod +x /start.sh

# Start
CMD ["/start.sh"]