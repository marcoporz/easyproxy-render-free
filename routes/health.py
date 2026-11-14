"""
Health routes - Health check per Render e monitoring.
"""
import logging
import os
import psutil
from aiohttp import web

logger = logging.getLogger(__name__)


def setup_health_routes(app):
    """Registra route per health check."""
    
    async def health_handler(request):
        """Health check endpoint per Render."""
        try:
            process = psutil.Process()
            mem = process.memory_info()
            mem_mb = round(mem.rss / 1024 / 1024, 1)
            
            return web.json_response({
                "status": "ok",
                "mode": "manifest-only",
                "memory_mb": mem_mb,
                "version": "2.0.0-manifest-only",
            })
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return web.json_response({
                "status": "degraded",
                "error": str(e),
            }, status=503)
    
    app.router.add_get("/health", health_handler)
    app.router.add_get("/healthz", health_handler)  # Alias per Kubernetes