#!/bin/bash
set -e

echo "=== Building EasyProxy Manifest-Only ==="

# Install system dependencies
apt-get update -qq
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

# Install FlareSolverr
echo "=== Installing FlareSolverr ==="
mkdir -p /opt/flaresolverr /opt/fsvenv
if [ ! -d "/opt/flaresolverr/.git" ]; then
    git clone --depth 1 --branch v3.5.2 https://github.com/FlareSolverr/FlareSolverr.git /opt/flaresolverr
fi
python3 -m venv /opt/fsvenv
/opt/fsvenv/bin/pip install --no-cache-dir setuptools wheel
/opt/fsvenv/bin/pip install --no-cache-dir -r /opt/flaresolverr/requirements.txt

# Install Python dependencies
echo "=== Installing Python dependencies ==="
pip install --no-cache-dir -r requirements.txt

echo "=== Build complete ==="