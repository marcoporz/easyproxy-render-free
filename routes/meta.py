"""
Meta routes - Metadati Stremio per film/serie/anime.
Supporta configurazione via base64 nell'URL, header X-API-Password, Authorization Bearer, query param pwd.
"""
import logging
from typing import Dict, Any
from aiohttp import web

from routes.utils import extract_config

logger = logging.getLogger(__name__)


def setup_meta_routes(app):
    """Registra route per meta Stremio."""
    
    async def meta_handler(request):
        """Handler per meta Stremio."""
        # Estrae config da tutte le fonti
        config = extract_config(request)
        
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