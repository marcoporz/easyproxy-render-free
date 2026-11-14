"""
Catalog routes - Cataloghi Stremio (anime, film, serie).
"""
import logging
import json
from typing import List, Dict
from aiohttp import web

logger = logging.getLogger(__name__)


def setup_catalog_routes(app):
    """Registra route per cataloghi Stremio."""
    
    async def catalog_handler(request):
        """Handler per cataloghi Stremio."""
        catalog_id = request.match_info.get("id", "")
        extra = request.query
        search = extra.get("search", "")
        skip = int(extra.get("skip", 0))
        genre = extra.get("genre", "")
        
        logger.info(f"Catalog request: {catalog_id}, search={search}, skip={skip}")
        
        # Import scraper
        from services.scraper_manager import get_scraper
        
        try:
            scraper = await get_scraper()
            
            if catalog_id.startswith("easyproxy-search"):
                if not search:
                    return web.json_response({"metas": []})
                
                # Determina tipo dalla catalog
                if catalog_id.endswith("-anime"):
                    meta_type = "anime"
                elif catalog_id.endswith("-series"):
                    meta_type = "series"
                else:
                    meta_type = "movie"
                
                results = await scraper.search(search, meta_type)
                metas = _convert_to_stremio_meta(results, meta_type)
                
            elif catalog_id.startswith("easyproxy-anime"):
                # Cataloghi anime Kitsu-style
                metas = await _get_anime_catalog(catalog_id, genre, skip)
            else:
                return web.json_response({"metas": []})
            
            # Paginazione
            metas = metas[skip:skip+20]
            
            return web.json_response({
                "metas": metas,
                "cacheMaxAge": 3600,
                "staleRevalidate": 3600,
                "staleError": 86400,
            })
            
        except Exception as e:
            logging.error(f"Catalog error: {e}")
            return web.json_response({"metas": []})
    
    app.router.add_get("/catalog/{id}.json", catalog_handler)


def _convert_to_stremio_meta(results: List[Dict], meta_type: str) -> List[Dict]:
    """Converte risultati scraper in formato Stremio Meta."""
    metas = []
    for r in results:
        if not r.get("title"):
            continue
        
        meta = {
            "id": r.get("id", "").replace(":", "-"),
            "type": meta_type,
            "name": r.get("title", ""),
            "poster": r.get("poster") or r.get("posterImage", ""),
            "background": r.get("background") or r.get("coverImage", ""),
        }
        
        # Aggiungi campi opzionali
        if r.get("description"):
            meta["description"] = r["description"]
        if r.get("year"):
            meta["year"] = str(r["year"])[:4]
        if r.get("genres"):
            meta["genres"] = r["genres"]
        
        metas.append(meta)
    
    return metas


async def _get_anime_catalog(catalog_id: str, genre: str, skip: int) -> List[Dict]:
    """Ottiene catalogo anime (Kitsu-style)."""
    # Implementazione semplificata - restituisce lista vuota
    # In produzione integrerebbe con Kitsu API
    return []