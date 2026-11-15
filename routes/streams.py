"""
Streams routes - Endpoint /stream/{type}/{id}.json per Stremio.
Restituisce lista di stream che passano per il nostro proxy headers-only.
"""
import logging
import json
import base64
import urllib.parse
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


def _build_stream_proxy_url(base_url: str, stream_url: str, referer: str = "", origin: str = "", ua: str = "", extra_headers: dict = None) -> str:
    """Costruisce URL del nostro stream proxy con parametri."""
    params = {"url": stream_url}
    if referer:
        params["referer"] = referer
    if origin:
        params["origin"] = origin
    if ua:
        params["ua"] = ua
    if extra_headers:
        params["headers"] = json.dumps(extra_headers)
    
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"{base_url}/stream/?{query}"


def setup_streams_routes(app):
    """Registra route per streams Stremio."""
    
    async def streams_handler(request):
        """Handler per /stream/{type}/{id}.json"""
        # Estrae config da path se presente
        b64config = request.match_info.get("config", "")
        config = _decode_config(b64config) if b64config else {}
        
        stream_type = request.match_info.get("type", "")
        stream_id = request.match_info.get("id", "")
        
        logger.info(f"Streams request: config_keys={list(config.keys())}, type={stream_type}, id={stream_id}")
        
        # Per ora restituiamo streams vuoti - i veri stream vengono estratti dai siti
        # quando l'utente clicca su un risultato di ricerca
        # I veri stream URLs vengono costruiti dal frontend (Easy Streams) o dal meta handler
        
        # Base URL per il proxy
        base_url = config.get("pub", "").rstrip("/")
        if not base_url:
            base_url = str(request.url).split("/stream/")[0]
        
        # NOTA: In una implementazione completa, qui si farebbe:
        # 1. Fetch meta dal sito sorgente usando stream_id
        # 2. Estrai stream URLs (m3u8, mp4, ecc.)
        # 3. Per ogni stream, costruisci URL proxy: /stream/?url=...&referer=...
        # 4. Restituisci lista streams
        
        # Per ora restituiamo array vuoto - Easy Streams gestisce gli stream
        return web.json_response({
            "streams": [],
            "cacheMaxAge": 3600,
            "staleRevalidate": 3600,
            "staleError": 86400,
        })
    
    # Route base (senza config)
    app.router.add_get("/stream/{type}/{id}.json", streams_handler)
    # Route con config base64: /<b64>/stream/{type}/{id}.json
    app.router.add_get("/{config}/stream/{type}/{id}.json", streams_handler)