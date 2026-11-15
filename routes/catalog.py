"""
Catalog routes - Cataloghi Stremio (anime, film, serie).
Supporta configurazione via base64 nell'URL, header X-API-Password, Authorization Bearer, query param pwd.
"""
import logging
from typing import List, Dict
from aiohttp import web

from routes.utils import extract_config

logger = logging.getLogger(__name__)


def setup_catalog_routes(app):
    """Registra route per cataloghi Stremio."""
    
    async def catalog_handler(request):
        """Handler per cataloghi Stremio."""
        # Estrae config da tutte le fonti
        config = extract_config(request)
        
        catalog_id = request.match_info.get("id", "")
        extra = request.query
        search = extra.get("search", "")
        skip = int(extra.get("skip", 0))
        genre = extra.get("genre", "")
        
        logger.info(f"Catalog request: config_keys={list(config.keys())}, catalog_id={catalog_id}, search={search}, skip={skip}")
        
        # Import scraper
        from services.scraper_manager import get_scraper
        
        try:
            scraper = await get_scraper()
            
            # Passa config allo scraper per Real-Debrid se presente
            if hasattr(scraper, 'set_config'):
                scraper.set_config(config)
            
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
    
    # Route base (senza config)
    app.router.add_get("/catalog/{id}.json", catalog_handler)
    # Route con config base64: /<b64>/catalog/{id}.json
    app.router.add_get("/{config}/catalog/{id}.json", catalog_handler)


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