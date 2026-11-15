"""
Shared utilities for routes - config extraction from multiple sources.
"""
import json
import logging
import base64
from aiohttp import web

logger = logging.getLogger(__name__)


def extract_config(request) -> dict:
    """
    Estrae configurazione da fonti multiple:
    1. base64 nel path (/<b64config>/...)
    2. header X-API-Password
    3. header Authorization: Bearer <token>
    4. query param ?pwd=<password>
    
    Ritorna dict con chiavi: pub, rd, pwd, etc.
    """
    config = {}
    
    # 1. Da base64 nel path
    b64config = request.match_info.get("config", "")
    if b64config:
        try:
            b64config = b64config.rstrip("=")
            padding = 4 - len(b64config) % 4
            if padding != 4:
                b64config += "=" * padding
            decoded = base64.urlsafe_b64decode(b64config).decode()
            config = json.loads(decoded)
        except Exception as e:
            logger.warning(f"Failed to decode base64 config: {e}")
    
    # 2. Da header X-API-Password (case-insensitive)
    api_pwd = request.headers.get("X-API-Password") or request.headers.get("x-api-password")
    if api_pwd:
        config["pwd"] = api_pwd
    
    # 3. Da Authorization: Bearer <token>
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        config["pwd"] = auth[7:]
    
    # 4. Da query param pwd
    pwd = request.query.get("pwd")
    if pwd:
        config["pwd"] = pwd
    
    return config