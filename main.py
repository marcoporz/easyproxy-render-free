#!/usr/bin/env python3
"""
EasyProxy Manifest-Only per Render Free Tier.
SOLO: manifest, catalog, meta, search, configure.
NESSUN proxy video/segmenti.
"""
import os
import sys
import asyncio
import logging
import json
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

# Configurazione logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    force=True,
)
logger = logging.getLogger(__name__)

# Aggiungi path per import moduli locali
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiohttp import web
from aiohttp.web import Request, Response, json_response

# Import config
from config import (
    PORT, FLARESOLVERR_URL, FLARESOLVERR_PORT, FLARESOLVERR_ENABLED,
    LOG_LEVEL, MANIFEST_ONLY, DISABLE_PROXY, DISABLE_HLS_PROXY,
    DISABLE_DASH_PROXY, DISABLE_RECORDING, LOG_LEVEL,
    FLARESOLVERR_ENABLED, FLARESOLVERR_PORT, FLARESOLVERR_URL,
    MANIFEST_ONLY, DISABLE_PROXY, DISABLE_HLS_PROXY,
    DISABLE_DASH_PROXY, DISABLE_RECORDING,
)

# Config logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    force=True,
)
logger = logging.getLogger(__name__)

# Disabilita log aiohttp verbose
logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
logging.getLogger("aiohttp.server").setLevel(logging.WARNING)

# Import moduli locali
from services.flaresolverr import FlareSolverrService
from services.scraper_manager import ScraperManager
from routes.manifest import setup_manifest_routes
from routes.catalog import setup_catalog_routes
from routes.meta import setup_meta_routes
from routes.search import setup_search_routes
from routes.configure import setup_configure_routes
from routes.health import setup_health_routes


async def init_flaresolverr():
    """Inizializza e avvia FlareSolverr per scraping Cloudflare."""
    import os
    if not os.environ.get("FLARESOLVERR_ENABLED", "true").lower() == "true":
        logger.info("FlareSolverr disabilitato")
        return
    
    from services.flaresolverr import FlareSolverrService
    global flaresolverr_service
    
    flaresolverr_service = FlareSolverrService()
    await flaresolverr_service.start()
    logger.info("FlareSolverr avviato")


async def cleanup_flaresolverr(app):
    """Cleanup FlareSolverr allo shutdown."""
    global flaresolverr_service
    if flaresolverr_service:
        await flaresolverr_service.stop()


def create_app():
    """Crea l'applicazione aiohttp SOLO per manifest/catalog/meta."""
    app = web.Application(client_max_size=4 * 1024 * 1024)
    
    # Middleware per logging richieste (solo warning/error)
    @web.middleware
    async def log_middleware(request, handler):
        start = time.time()
        response = None
        try:
            response = await handler(request)
            return response
        except Exception:
            raise
        finally:
            if response and response.status >= 400:
                logger.warning(
                    "%s %s -> %s (%.0fms)",
                    request.method, request.path, response.status,
                    (time.time() - start) * 1000
                )
    
    app.middlewares.append(log_middleware)
    
    # CORS headers
    @web.middleware
    async def cors_middleware(request, handler):
        if request.method == "OPTIONS":
            return web.Response(
                status=204,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                }
            )
        response = await handler(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    
    app.middlewares.append(cors_middleware)
    
    # Endpoint info base
    async def info_handler(request):
        return json_response({
            "name": "EasyProxy Manifest-Only",
            "version": "2.0.0-manifest-only",
            "mode": "manifest-only",
            "description": "Solo manifest/catalog/meta - NESSUN proxy video",
            "endpoints": {
                "manifest": "/manifest.json",
                "configure": "/configure",
                "catalog": "/catalog/*",
                "meta": "/meta/*",
                "search": "/search",
                "health": "/health",
            },
            "disabled": [
                "proxy video/segmenti",
                "HLS proxy",
                "DASH proxy",
                "recording/DVR",
                "torrent download",
            ],
            "flaresolverr": "Solo per scraping Cloudflare durante catalog/search",
        })
    
    # Registra route SOLO per manifest/catalog/meta/configure/health
    setup_manifest_routes(app)
    setup_catalog_routes(app)
    setup_meta_routes(app)
    setup_search_routes(app)
    setup_configure_routes(app)
    setup_health_routes(app)
    
    app.router.add_get("/", info_handler)
    app.router.add_get("/info", info_handler)
    
    # Health check per Render
    async def health_handler(request):
        return json_response({
            "status": "ok",
            "mode": "manifest-only",
            "memory_mb": get_memory_usage(),
        })
    
    app.router.add_get("/health", health_handler)
    
    return app


async def on_startup(app):
    """Avvio servizi."""
    logger.info("=== Avvio EasyProxy Manifest-Only ===")
    
    # Avvia FlareSolverr solo per scraping
    await init_flaresolverr()
    
    logger.info(f"=== EasyProxy Manifest-Only avviato su porta {PORT} ===")


async def on_cleanup(app):
    """Cleanup allo shutdown."""
    logger.info("=== Shutdown ===")
    await cleanup_flaresolverr(app)


# Variabili globali
PORT = int(os.environ.get("PORT", 10000))
flaresolverr_service = None


def get_memory_usage():
    """Restituisce uso memoria in MB."""
    try:
        import psutil
        process = psutil.Process()
        mem = process.memory_info()
        return round(process.memory_info().rss / 1024 / 1024, 1)
    except Exception:
        return 0


def main():
    """Entry point."""
    logger.info("=== EasyProxy Manifest-Only per Render Free ===")
    logger.info(f"Porta: {PORT}")
    logger.info("Modalità: Manifest-Only (nessun proxy video)")
    
    app = create_app()
    
    # Registra eventi startup/shutdown
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    
    # Avvia server
    web.run_app(
        app,
        host="0.0.0.0",
        port=PORT,
        access_log=None,  # Disabilita access log per risparmiare RAM
    )


if __name__ == "__main__":
    main()