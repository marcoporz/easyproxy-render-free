#!/bin/bash
set -e

# Configuration
export PORT=${PORT:-10000}
export FLARESOLVERR_PORT=8191
export FLARESOLVERR_URL="http://127.0.0.1:8191"
export LOG_LEVEL=WARNING
export MANIFEST_ONLY=true
export DISABLE_PROXY=true
export DISABLE_HLS_PROXY=true
export DISABLE_DASH_PROXY=true
export DISABLE_RECORDING=true
export LOG_LEVEL=WARNING

# Logging
log() {
    echo "[$(date '+%H:%M:%S')] $*"
}

# Start FlareSolverr
start_flaresolverr() {
    log "Starting FlareSolverr on port 8191..."
    
    cd /opt/flaresolverr
    PORT=8191 HOST=127.0.0.1 LOG_LEVEL=ERROR LOG_HTML=false \
    PYTHONPATH=/opt/flaresolverr/src \
    /opt/fsvenv/bin/python -u src/flaresolverr.py &
    FLARESOLVERR_PID=$!
    
    # Wait for FlareSolverr to be ready
    for i in {1..30}; do
        if curl -sf "http://127.0.0.1:8191/v1" >/dev/null 2>&1; then
            echo "=== FLARESOLVERR READY ==="
            return 0
        fi
        sleep 1
    done
    
    echo "ERROR: FlareSolverr failed to start"
    exit 1
}

# Main
main() {
    log "=== Starting EasyProxy Manifest-Only on Render Free ==="
    log "Port: ${PORT:-10000}"
    log "Mode: Manifest-Only (no video proxy)"
    
    # Start FlareSolverr
    start_flaresolverr
    
    # Start EasyProxy
    log "Starting EasyProxy Manifest-Only on port ${PORT:-10000}..."
    
    export PORT=${PORT:-10000}
    export FLARESOLVERR_URL="http://127.0.0.1:8191"
    export LOG_LEVEL=WARNING
    export MANIFEST_ONLY=true
    export DISABLE_PROXY=true
    export DISABLE_HLS_PROXY=true
    export DISABLE_DASH_PROXY=true
    export DISABLE_RECORDING=true
    export LOG_LEVEL=WARNING
    
    # Run the app
    exec python3 main.py
}

# Trap signals
trap 'echo "Shutting down..."; kill 0; exit 0' SIGTERM SIGINT

main