#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from config import PORT, MANIFEST_ONLY, DISABLE_PROXY
print(f'PORT={PORT}')
print(f'MANIFEST_ONLY={MANIFEST_ONLY}')
print(f'DISABLE_PROXY={DISABLE_PROXY}')

from main import create_app
print('main.py imports OK')

from routes.manifest import setup_manifest_routes
from routes.catalog import setup_catalog_routes
from routes.meta import setup_meta_routes
from routes.search import setup_search_routes
from routes.configure import setup_configure_routes
from routes.health import setup_health_routes
print('All routes import OK')

from services.flaresolverr import FlareSolverrService
from services.scraper_manager import get_scraper, ScraperManager
print('Services import OK')
print('All imports OK!')