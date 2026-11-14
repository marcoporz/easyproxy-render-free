"""
FlareSolverr Service - Solo per scraping Cloudflare durante catalog/search.
Non usato per proxy video.
"""
import asyncio
import logging
import subprocess
import time
import urllib.request
import os
import signal

logger = logging.getLogger(__name__)


class FlareSolverrService:
    """Gestisce FlareSolverr per bypass Cloudflare durante scraping."""
    
    def __init__(self):
        self.process = None
        self.port = int(os.environ.get("FLARESOLVERR_PORT", 8191))
        self.url = f"http://127.0.0.1:{self.port}"
        self.process_handle = None
        self._ready = False
        
    async def start(self):
        """Avvia FlareSolverr."""
        if self._ready:
            return
            
        logger.info("Avvio FlareSolverr...")
        
        # Verifica se già in esecuzione
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/v1", timeout=2) as resp:
                if resp.status == 200:
                    logger.info("FlareSolverr già in esecuzione")
                    self._ready = True
                    return
        except Exception:
            pass
        
        # Avvia FlareSolverr
        cmd = [
            "python3", "-m", "flaresolverr",
            "--port", str(os.environ.get("FLARESOLVERR_PORT", 8191)),
            "--host", "127.0.0.1",
        ]
        
        env = os.environ.copy()
        env.update({
            "PORT": str(os.environ.get("FLARESOLVERR_PORT", 8191)),
            "HOST": "127.0.0.1",
            "LOG_LEVEL": "ERROR",
            "LOG_HTML": "false",
            "HEADLESS": "true",
        })
        
        self.process = subprocess.Popen(
            ["python3", "-m", "flaresolverr"],
            cwd="/opt/flaresolverr" if os.path.exists("/opt/flaresolverr") else ".",
            env={**os.environ, **{
                "PORT": "8191",
                "HOST": "127.0.0.1",
                "LOG_LEVEL": "ERROR",
                "LOG_HTML": "false",
                "HEADLESS": "true",
            }},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        
        # Wait for ready
        for i in range(30):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:8191/v1", timeout=2) as resp:
                    if resp.status == 200:
                        logger.info("FlareSolverr pronto")
                        return
            except Exception:
                pass
            await asyncio.sleep(1)
        
        raise RuntimeError("FlareSolverr failed to start")
    
    async def solve(self, url, method="GET", headers=None, post_data=None, timeout=30):
        """Risolve una URL protetta da Cloudflare."""
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": timeout * 1000,
        }
        if method == "POST":
            payload["cmd"] = "request.post"
            if post_data:
                payload["postData"] = post_data
        if headers:
            payload["headers"] = headers
        
        url = f"{self.url}/v1"
        try:
            req = urllib.request.Request(
                self.url,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: urllib.request.urlopen(
                    req, timeout=timeout
                ).read()
            )
            result = json.loads(response.decode())
            if result.get("status") == "ok":
                return result.get("solution", {})
            else:
                logger.error(f"FlareSolverr error: {result.get('message')}")
                return None
        except Exception as e:
            logger.error(f"FlareSolverr error: {e}")
            return None
    
    async def stop(self):
        """Ferma FlareSolverr."""
        if self.process:
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()


# Istanza globale
flaresolverr_service = None


async def init_flaresolverr():
    """Inizializza FlareSolverr."""
    global flaresolverr_service
    
    if not os.environ.get("FLARESOLVERR_ENABLED", "true").lower() == "true":
        logger.info("FlareSolverr disabilitato")
        return
    
    logger.info("Avvio FlareSolverr...")
    global flaresolverr_service
    
    # Verifica se già in esecuzione
    try:
        with urllib.request.urlopen("http://127.0.0.1:8191/v1", timeout=2) as resp:
            if resp.status == 200:
                logger.info("FlareSolverr già in esecuzione")
                return
    except Exception:
        pass
    
    # Avvia FlareSolverr
    env = os.environ.copy()
    env.update({
        "PORT": "8191",
        "HOST": "127.0.0.1",
        "LOG_LEVEL": "ERROR",
        "LOG_HTML": "false",
        "HEADLESS": "true",
    })
    
    # Avvia in background
    process = subprocess.Popen(
        ["python3", "-m", "flaresolverr"],
        env={**os.environ, **{
            "PORT": "8191",
            "HOST": "127.0.0.1",
            "LOG_LEVEL": "ERROR",
            "LOG_HTML": "false",
            "HEADLESS": "true",
        }},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    
    # Wait for ready
    for i in range(30):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8191/v1", timeout=2) as resp:
                if resp.status == 200:
                    logger.info("FlareSolverr pronto")
                    return
        except Exception:
            pass
        await asyncio.sleep(1)
    
    raise RuntimeError("FlareSolverr failed to start")


async def cleanup_flaresolverr(app):
    """Cleanup FlareSolverr."""
    logger.info("Stopping FlareSolverr...")
    # FlareSolverr runs in background, will be killed with process
    pass