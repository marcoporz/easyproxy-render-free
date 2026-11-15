"""
Manifest routes - Genera manifest Stremio per l'addon.
Supporta configurazione via:
- base64 nell'URL: /<b64config>/manifest.json
- header X-API-Password / Authorization: Bearer <pwd>
- query param ?pwd=<password>
"""
import json
import logging
import os
import base64
from aiohttp import web

from config import PUBLIC_HOST, MANIFEST_ONLY

logger = logging.getLogger(__name__)


def _extract_config(request) -> dict:
    """Estrae config da vari fonti: base64 path, header, query param."""
    config = {}
    
    # 1. Da base64 nel path
    b64config = request.match_info.get("config", "")
    if b64config:
        try:
            b64config = b64config.rstrip("=")
            padding = 4 - len(b64config) % 4
            if padding != 4:
                b64config += "=" * padding
            decoded = base64.urlsafe_b64decode(b64config).decode()
            config = json.loads(decoded)
        except Exception as e:
            logger.warning(f"Failed to decode base64 config: {e}")
    
    # 2. Da header X-API-Password
    api_pwd = request.headers.get("X-API-Password") or request.headers.get("x-api-password")
    if api_pwd:
        config["pwd"] = api_pwd
    
    # 3. Da Authorization: Bearer <token>
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        config["pwd"] = auth[7:]
    
    # 4. Da query param pwd
    pwd = request.query.get("pwd")
    if pwd:
        config["pwd"] = pwd
    
    return config


def setup_manifest_routes(app):
    """Registra route per manifest Stremio."""
    
    async def manifest_handler(request):
        """Genera manifest Stremio con config da fonti multiple."""
        config = _extract_config(request)
        
        manifest = {
            "id": "org.easyproxy.manifest-only",
            "version": "2.0.0-manifest-only",
            "name": "EasyProxy Manifest-Only",
            "description": "Manifest/catalog/meta + stream proxy headers-only. Proxy URL: base URL, Password: via header X-API-Password.",
            "logo": f"{PUBLIC_HOST}/logo.png" if os.environ.get("PUBLIC_HOST") else "",
            "background": f"{PUBLIC_HOST}/background.png" if os.environ.get("PUBLIC_HOST") else "",
            "resources": ["catalog", "meta", "stream"],
            "types": ["movie", "series", "anime"],
            "idPrefixes": [
                "tt", "kitsu", "mal", "anilist", "anidb", 
                "tmdb", "themoviedb", "tvdb", "thetvdb", "cr", "crunchyroll"
            ],
            "catalogs": [
                {"id": "easyproxy-search", "type": "movie", "name": "EasyProxy Search", "extra": [{"name": "search", "isRequired": True}]},
                {"id": "easyproxy-search", "type": "series", "name": "EasyProxy Search", "extra": [{"name": "search", "isRequired": True}]},
                {"id": "easyproxy-search", "type": "anime", "name": "EasyProxy Search", "extra": [{"name": "search", "isRequired": True}]},
            ],
            "behaviorHints": {
                "configurable": True,
                "configurationRequired": False
            }
        }
        
        # Aggiungi info config nel description
        if config.get("pub"):
            manifest["description"] += f" | Config: {config['pub']}"
        if config.get("rd"):
            manifest["description"] += " | Real-Debrid: ✓"
        if config.get("pwd"):
            manifest["description"] += " | Password: ✓"
        
        return web.json_response(manifest)
    
    # Route base (senza config path)
    app.router.add_get("/manifest.json", manifest_handler)
    # Route con config base64: /<b64>/manifest.json
    app.router.add_get("/{config}/manifest.json", manifest_handler)


# Import at bottom to avoid circular imports
import os
import logging

logger = logging.getLogger(__name__)