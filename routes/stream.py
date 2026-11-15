"""
Stream routes - Proxy per stream con headers/referer.
Aggiunge headers necessari e fa redirect 302 al CDN.
Banda usata: ~1KB per redirect (non segmenti video).
Supporta configurazione via base64 nell'URL, header X-API-Password, Authorization Bearer, query param pwd.
"""
import json
import logging
import urllib.parse
from aiohttp import web

from routes.utils import extract_config

logger = logging.getLogger(__name__)


def setup_stream_routes(app):
    """Registra route per stream proxy."""
    
    async def stream_handler(request):
        """
        Stream proxy endpoint.
        
        Query params:
        - url: URL dello stream (required)
        - referer: Referer header (opzionale)
        - origin: Origin header (opzionale)
        - ua: User-Agent personalizzato (opzionale)
        - headers: JSON encoded extra headers (opzionale)
        
        Fa redirect 302 all'URL con headers appropriati.
        """
        # Estrae config da tutte le fonti
        config = extract_config(request)
        
        stream_url = request.query.get("url", "")
        referer = request.query.get("referer", "")
        origin = request.query.get("origin", "")
        ua = request.query.get("ua", "")
        extra_headers_json = request.query.get("headers", "{}")
        
        if not stream_url:
            logger.warning("Stream request without URL")
            return web.Response(status=400, text="Missing 'url' parameter")
        
        # Decodifica URL se encodato
        try:
            stream_url = urllib.parse.unquote(stream_url)
        except Exception:
            pass
        
        # Prepara headers per il redirect
        redirect_headers = {
            "Location": stream_url,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "Range, Content-Type, Authorization",
            "Cache-Control": "no-cache, no-store, must-revalidate",
        }
        
        # Aggiunge Referer se fornito
        if referer:
            try:
                referer = urllib.parse.unquote(referer)
                redirect_headers["Referer"] = referer
            except Exception:
                pass
        
        # Aggiunge Origin se fornito
        if origin:
            try:
                origin = urllib.parse.unquote(origin)
                redirect_headers["Origin"] = origin
            except Exception:
                pass
        
        # Aggiunge User-Agent se fornito
        if ua:
            try:
                ua = urllib.parse.unquote(ua)
                redirect_headers["User-Agent"] = ua
            except Exception:
                pass
        
        # Aggiunge extra headers da JSON
        try:
            extra_headers = json.loads(extra_headers_json)
            if isinstance(extra_headers, dict):
                for k, v in extra_headers.items():
                    redirect_headers[k] = v
        except Exception:
            pass
        
        # Log per debug
        logger.info(f"Stream redirect: {stream_url[:100]}... | Referer: {referer[:50] if referer else 'none'} | Config keys: {list(config.keys())}")
        
        # Redirect 302 con headers - usa HTTPFound per redirect corretto
        response = web.HTTPFound(location=stream_url)
        # Aggiunge headers extra
        for k, v in redirect_headers.items():
            if k != "Location":  # Location è gestito da HTTPFound
                response.headers[k] = v
        return response
    
    async def stream_options(request):
        """Handle CORS preflight."""
        return web.Response(
            status=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
                "Access-Control-Allow-Headers": "Range, Content-Type, Authorization, Referer, Origin",
                "Access-Control-Max-Age": "86400",
            }
        )
    
    # Route base (senza config)
    app.router.add_get("/stream/", stream_handler)
    app.router.add_options("/stream/", stream_options)
    
    # Route con config base64: /<b64>/stream/
    app.router.add_get("/{config}/stream/", stream_handler)
    app.router.add_options("/{config}/stream/", stream_options)