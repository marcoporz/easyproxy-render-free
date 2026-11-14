"""
Scraper Manager - Gestisce scraping per cataloghi/ricerca SENZA proxy video.
Usa FlareSolverr solo per siti Cloudflare durante catalog/search.
"""
import asyncio
import logging
import json
import re
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urljoin, urlparse
from datetime import datetime, timedelta

import aiohttp
from aiohttp import ClientSession, ClientTimeout

logger = logging.getLogger(__name__)


class ScraperManager:
    """Gestisce scraping per cataloghi/ricerca SENZA proxy video."""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache = {}
        self.flaresolverr_url = "http://127.0.0.1:8191"
        
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=3,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
        )
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _fetch_with_flare(self, url: str, method: str = "GET", **kwargs) -> Optional[str]:
        """Fetch con fallback a FlareSolverr per Cloudflare."""
        # Prima prova richiesta diretta
        try:
            async with self.session.request(method, url, timeout=10) as resp:
                if resp.status == 200:
                    return await resp.text()
                if resp.status in (403, 503) and "cloudflare" in (await resp.text()).lower():
                    logger.info(f"Cloudflare detected on {url}, trying FlareSolverr")
                    return await self._flare_solve(url)
        except Exception as e:
            logger.warning(f"Direct fetch failed for {url}: {e}")
            # Prova FlareSolverr come fallback
            return await self._flare_solve(url)
        return None
    
    async def _flare_solve(self, url: str) -> Optional[str]:
        """Usa FlareSolverr per bypassare Cloudflare."""
        try:
            payload = {
                "cmd": "request.get",
                "url": url,
                "maxTimeout": 30000,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://127.0.0.1:8191/v1",
                    json={"cmd": "request.get", "url": url, "maxTimeout": 30000},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "ok":
                            return data.get("solution", {}).get("response")
        except Exception as e:
            logger.warning(f"FlareSolverr failed for {url}: {e}")
        return None
    
    async def search_animeworld(self, query: str, page: int = 1) -> List[Dict]:
        """Cerca su AnimeWorld."""
        url = f"https://www.animeworld.ac/api/search?keyword={quote(query)}"
        html = await self._fetch_with_flare(url)
        if not html:
            return []
        
        # Parse results from AnimeWorld API response
        try:
            data = json.loads(html)
            items = data.get("data", [])
            results = []
            for item in items[:20]:
                results.append({
                    "id": item.get("slug", ""),
                    "title": item.get("title", ""),
                    "poster": item.get("poster", ""),
                    "type": "anime",
                })
            return results
        except Exception:
            return []
    
    async def search_animesaturn(self, query: str, page: int = 1) -> List[Dict]:
        """Cerca su AnimeSaturn."""
        url = f"https://www.animesaturn.cx/animelist?search={quote(query)}"
        html = await self._fetch_with_flare(url)
        if not html:
            return []
        
        results = []
        # Parse HTML results
        for match in re.finditer(r'href="/anime/([^"]+)"[^>]*>([^<]+)', html):
            slug, title = match.groups()
            results.append({
                "id": slug,
                "title": title.strip(),
                "type": "anime",
            })
        return results[:20]
    
    async def search_streamingcommunity(self, query: str, page: int = 1) -> List[Dict]:
        """Cerca su StreamingCommunity."""
        # StreamingCommunity usa API TMDB-like
        results = []
        # Implementazione semplificata
        return results
    
    async def _fetch_with_flare(self, url: str) -> Optional[str]:
        """Fetch con fallback a FlareSolverr."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    if resp.status in (403, 503):
                        # Prova FlareSolverr
                        return await self._flare_solve(url)
        except Exception:
            pass
        return await self._flare_solve(url)
    
    async def _flare_solve(self, url: str) -> Optional[str]:
        """Risolve via FlareSolverr."""
        try:
            payload = {"cmd": "request.get", "url": url, "maxTimeout": 30000}
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://127.0.0.1:8191/v1",
                    json={"cmd": "request.get", "url": url, "maxTimeout": 30000},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "ok":
                            return data.get("solution", {}).get("response")
        except Exception as e:
            logger.warning(f"FlareSolverr failed for {url}: {e}")
        return None

    async def search(self, query: str, type: str = "all") -> List[Dict]:
        """Ricerca unificata su tutte le fonti."""
        tasks = [
            self.search_animeworld(query),
            self.search_animesaturn(query),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_results = []
        for result in results:
            if isinstance(result, list):
                all_results.extend(result)
        
        # Deduplica per titolo
        seen = set()
        unique = []
        for r in all_results:
            key = r.get("title", "").lower()
            if key and key not in seen:
                seen.add(key)
                unique.append(r)
        
        return unique[:30]


# Cache semplice in memoria
class MemoryCache:
    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Any:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        if len(self.cache) >= 1000:
            # Rimuovi il più vecchio
            oldest = min(self.cache.items(), key=lambda x: x[1][1])
            del self.cache[oldest[0]]
        self.cache[key] = (value, time.time())


# Istanza globale cache
cache = MemoryCache(ttl=3600)


async def get_scraper() -> ScraperManager:
    """Factory per ScraperManager."""
    scraper = ScraperManager()
    await scraper.__aenter__()
    return scraper