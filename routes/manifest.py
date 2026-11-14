"""
Manifest routes - Genera manifest Stremio per l'addon.
"""
import json
import logging
import os
from aiohttp import web

from config import PUBLIC_HOST, MANIFEST_ONLY

logger = logging.getLogger(__name__)


def setup_manifest_routes(app):
    """Registra route per manifest Stremio."""
    
    async def manifest_handler(request):
        """Genera manifest Stremio."""
        manifest = {
            "id": "org.easyproxy.manifest-only",
            "version": "2.0.0-manifest-only",
            "name": "EasyProxy Manifest-Only",
            "description": "Solo manifest/catalog/meta - NESSUN proxy video. Stream diretti da CDN.",
            "logo": f"{PUBLIC_HOST}/logo.png" if os.environ.get("PUBLIC_HOST") else "",
            "background": f"{PUBLIC_HOST}/background.png" if os.environ.get("PUBLIC_HOST") else "",
            "resources": ["catalog", "meta", "stream"],
            "types": ["movie", "series", "anime"],
            "idPrefixes": [
                "tt", "kitsu", "mal", "anilist", "anidb", 
                "tmdb", "themoviedb", "tvdb", "thetvdb", "cr", "crunchyroll"
            ],
            "catalogs": [
                {
                    "id": "easyproxy-search",
                    "type": "movie",
                    "name": "EasyProxy Search",
                    "extra": [{"name": "search", "isRequired": True}],
                },
                {
                    "id": "easyproxy-search",
                    "type": "series",
                    "name": "EasyProxy Search",
                    "extra": [{"name": "search", "isRequired": True}],
                },
                {
                    "id": "easyproxy-search",
                    "type": "anime",
                    "name": "EasyProxy Search",
                    "extra": [{"name": "search", "isRequired": True}],
                },
            ],
            "behaviorHints": {
                "configurable": True,
                "configurationRequired": False
            }
        }
        return web.json_response(manifest)
    
    app.router.add_get("/manifest.json", manifest_handler)


# Import at bottom to avoid circular imports
import os
import logging

logger = logging.getLogger(__name__)