"""
Manifest routes - Genera manifest Stremio per l'addon.
Supporta configurazione via base64 nell'URL: /<b64config>/manifest.json
"""
import json
import logging
import os
import base64
from aiohttp import web

from config import PUBLIC_HOST, MANIFEST_ONLY

logger = logging.getLogger(__name__)


def setup_manifest_routes(app):
    """Registra route per manifest Stremio."""
    
    async def manifest_handler(request):
        """Genera manifest Stremio base."""
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
    
    async def manifest_config_handler(request):
        """Genera manifest Stremio con configurazione da base64 nell'URL."""
        # Decodifica config da base64 nel path
        b64config = request.match_info.get("config", "")
        config = {}
        
        if b64config:
            try:
                # Rimuovi padding se presente
                b64config = b64config.rstrip("=")
                # Aggiungi padding corretto
                padding = 4 - len(b64config) % 4
                if padding != 4:
                    b64config += "=" * padding
                decoded = base64.urlsafe_b64decode(b64config).decode()
                config = json.loads(decoded)
                logger.info(f"Manifest config loaded: pub={'pub' in config}, rd={'rd' in config}, pwd={'pwd' in config}")
            except Exception as e:
                logger.warning(f"Failed to decode manifest config: {e}")
        
        # Base manifest
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
        
        # Aggiungi info config nel description se presente
        if config.get("pub"):
            manifest["description"] += f" | Config: {config['pub']}"
        if config.get("rd"):
            manifest["description"] += " | Real-Debrid: ✓"
        if config.get("pwd"):
            manifest["description"] += " | Password: ✓"
        
        return web.json_response(manifest)
    
    # Route base (senza config)
    app.router.add_get("/manifest.json", manifest_handler)
    # Route con config base64: /<b64>/manifest.json
    app.router.add_get("/{config}/manifest.json", manifest_config_handler)


# Import at bottom to avoid circular imports
import os
import logging

logger = logging.getLogger(__name__)