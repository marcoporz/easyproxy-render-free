"""
Meta routes - Metadati Stremio per film/serie/anime.
Supporta configurazione via base64 nell'URL: /<b64config>/meta/{type}/{id}.json
"""
import logging
import json
import base64
from typing import Dict, Any
from aiohttp import web

logger = logging.getLogger(__name__)


def _decode_config(b64config: str) -> dict:
    """Decodifica config da base64 URL-safe."""
    if not b64config:
        return {}
    try:
        b64config = b64config.rstrip("=")
        padding = 4 - len(b64config) % 4
        if padding != 4:
            b64config += "=" * padding
        decoded = base64.urlsafe_b64decode(b64config).decode()
        return json.loads(decoded)
    except Exception:
        return {}


def setup_meta_routes(app):
    """Registra route per meta Stremio."""
    
    async def meta_handler(request):
        """Handler per meta Stremio."""
        # Estrae config da path se presente
        b64config = request.match_info.get("config", "")
        config = _decode_config(b64config)
        
        meta_type = request.match_info.get("type", "")
        meta_id = request.match_info.get("id", "")
        
        logger.info(f"Meta request: config_keys={list(config.keys())}, type={meta_type}, id={meta_id}")
        
        # Per ora restituisce meta vuoto - Stremio userà Cinemeta/altri addon
        # In produzione integrerebbe con Cinemeta/TMDB/Kitsu
        return web.json_response({"meta": None})
    
    # Route base (senza config)
    app.router.add_get("/meta/{type}/{id}.json", meta_handler)
    # Route con config base64: /<b64>/meta/{type}/{id}.json
    app.router.add_get("/{config}/meta/{type}/{id}.json", meta_handler)