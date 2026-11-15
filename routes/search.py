"""
Search routes - Ricerca unificata per Stremio.
Supporta configurazione via base64 nell'URL: /<b64config>/search
"""
import logging
import json
import base64
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


def setup_search_routes(app):
    """Registra route per ricerca Stremio."""
    
    async def search_handler(request):
        """Handler per ricerca Stremio."""
        # Estrae config da path se presente
        b64config = request.match_info.get("config", "")
        config = _decode_config(b64config)
        
        search_query = request.query.get("search", "")
        
        logger.info(f"Search request: config_keys={list(config.keys())}, search={search_query}")
        
        if not search_query:
            return web.json_response({"metas": []})
        
        # Import scraper
        from services.scraper_manager import get_scraper
        
        try:
            scraper = await get_scraper()
            
            # Passa config allo scraper per Real-Debrid se presente
            if hasattr(scraper, 'set_config'):
                scraper.set_config(config)
            
            results = await scraper.search(search_query)
            metas = _convert_to_stremio_meta(results)
            
            return web.json_response({
                "metas": metas[:30],
                "cacheMaxAge": 3600,
                "staleRevalidate": 3600,
                "staleError": 86400,
            })
        except Exception as e:
            logging.error(f"Search error: {e}")
            return web.json_response({"metas": []})
    
    # Route base (senza config)
    app.router.add_get("/search", search_handler)
    # Route con config base64: /<b64>/search
    app.router.add_get("/{config}/search", search_handler)


def _convert_to_stremio_meta(results: list) -> list:
    """Converte risultati scraper in formato Stremio Meta."""
    metas = []
    for r in results:
        if not r.get("title"):
            continue
        
        # Determina tipo
        meta_type = "movie"
        if r.get("type") == "anime" or "anime" in r.get("id", "").lower():
            meta_type = "anime"
        elif r.get("type") == "series":
            meta_type = "series"
        
        meta = {
            "id": r.get("id", "").replace(":", "-"),
            "type": meta_type,
            "name": r.get("title", ""),
            "poster": r.get("poster") or r.get("posterImage", ""),
            "background": r.get("background") or r.get("coverImage", ""),
        }
        
        if r.get("description"):
            meta["description"] = r["description"]
        if r.get("year"):
            meta["year"] = str(r["year"])[:4]
        if r.get("genres"):
            meta["genres"] = r["genres"]
        
        metas.append(meta)
    
    return metas