"""
Meta routes - Metadati Stremio per film/serie/anime.
"""
import logging
from typing import Dict, Any
from aiohttp import web

logger = logging.getLogger(__name__)


def setup_meta_routes(app):
    """Registra route per meta Stremio."""
    
    async def meta_handler(request):
        """Handler per meta Stremio."""
        meta_type = request.match_info.get("type", "")
        meta_id = request.match_info.get("id", "")
        
        logger.info(f"Meta request: type={meta_type}, id={meta_id}")
        
        # Per ora restituisce meta vuoto - Stremio userà Cinemeta/altri addon
        # In produzione integrerebbe con Cinemeta/TMDB/Kitsu
        return web.json_response({"meta": None})
    
    app.router.add_get("/meta/{type}/{id}.json", meta_handler)