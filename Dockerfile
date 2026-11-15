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

# Create startup script
RUN echo '#!/bin/bash\nset -e\n\necho "=== Starting Xvfb ==="\nXvfb :99 -screen 0 1024x768x24 > /tmp/xvfb.log 2>&1 &\nXVFB_PID=$!\nexport DISPLAY=:99\nsleep 3\n\nif ! kill -0 $XVFB_PID 2>/dev/null; then\n    echo "ERROR: Xvfb died"\n    cat /tmp/xvfb.log\n    exit 1\nfi\necho "Xvfb running (PID: $XVFB_PID)"\n\necho "=== Starting FlareSolverr on port 8191 ==="\ncd /opt/flaresolverr\nPORT=8191 HOST=127.0.0.1 LOG_LEVEL=DEBUG LOG_HTML=false \\\nPYTHONPATH=/opt/flaresolverr/src \\\n/opt/fsvenv/bin/python -u src/flaresolverr.py > /tmp/flaresolverr.log 2>&1 &\nFLARESOLVERR_PID=$!\n\necho "FlareSolverr PID: $FLARESOLVERR_PID"\nsleep 5\n\necho "Waiting for FlareSolverr to be ready..."\nfor i in {1..60}; do\n    if curl -sf "http://127.0.0.1:8191/v1" >/dev/null 2>&1; then\n        echo "=== FLARESOLVERR READY ==="\n        break\n    fi\n    if ! kill -0 $FLARESOLVERR_PID 2>/dev/null; then\n        echo "ERROR: FlareSolverr process died"\n        echo "--- FlareSolverr log ---"\n        cat /tmp/flaresolverr.log\n        echo "--- Xvfb log ---"\n        cat /tmp/xvfb.log\n        exit 1\n    fi\n    if [ $((i % 10)) -eq 0 ]; then\n        echo "  Still waiting... ($i/60s)"\n        echo "  FlareSolverr log tail:"\n        tail -20 /tmp/flaresolverr.log\n    fi\n    sleep 1\ndone\n\nif ! curl -sf "http://127.0.0.1:8191/v1" >/dev/null 2>&1; then\n    echo "ERROR: FlareSolverr failed to start after 60s"\n    echo "--- FlareSolverr log ---"\n    cat /tmp/flaresolverr.log\n    echo "--- Xvfb log ---"\n    cat /tmp/xvfb.log\n    exit 1\nfi\n\necho "=== Starting EasyProxy Manifest-Only on port 10000 ==="\ncd /app\nexport PORT=10000\nexport FLARESOLVERR_URL="http://127.0.0.1:8191"\nexport LOG_LEVEL=WARNING\nexport MANIFEST_ONLY=true\nexport DISABLE_PROXY=true\nexport DISABLE_HLS_PROXY=true\nexport DISABLE_DASH_PROXY=true\nexport DISABLE_RECORDING=true\n\n# Trap signals to kill processes on exit\ntrap "kill $FLARESOLVERR_PID $XVFB_PID 2>/dev/null; exit 0" SIGTERM SIGINT\n\nexec python3 main.py' > /start.sh && chmod +x /start.sh

# Start
CMD ["/start.sh"]