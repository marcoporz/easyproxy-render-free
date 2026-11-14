"""
Configurazione Manifest-Only per Render Free Tier.
SOLO manifest/catalog/meta - NESSUN proxy segmenti video.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# === RENDER FREE TIER LIMITS ===
PORT = int(os.environ.get("PORT", 10000))  # Render usa 10000
MAX_MEMORY_MB = 512  # Render Free limit

# Public host per manifest URLs
PUBLIC_HOST = os.environ.get("PUBLIC_HOST", "")

# === MANIFEST-ONLY MODE ===
# Disabilita TUTTI i proxy segmenti/video
MANIFEST_ONLY = True
DISABLE_PROXY = True
DISABLE_HLS_PROXY = True
DISABLE_DASH_PROXY = True
DISABLE_RECORDING = True

# === FLARESOLVERR (solo per scraping Cloudflare) ===
FLARESOLVERR_URL = os.environ.get("FLARESOLVERR_URL", "http://127.0.0.1:8191")
FLARESOLVERR_ENABLED = True  # Solo per scraping Cloudflare durante catalog/search

# === RAM OPTIMIZATION ===
# Disabilita tutto ciò che consuma RAM
DISABLE_RECORDING = True
DISABLE_WEBHOOKS = True
DISABLE_SPEEDTEST = True
DISABLE_DVR = True
DISABLE_WARP = True
DISABLE_TOR = True
DISABLE_NORDVPN = True
DISABLE_CUSTOM_PROXIES = True

# === PROXY CONFIG ===
# BLOCCA TUTTI i domini video per evitare proxy segmenti
PROXY_EXCLUDE_DOMAINS = [
    # CDN video principali
    "vix-content.net", "vixsrc.to", "vixsrc.net", "vixsrc.cc",
    "vixcloud.co", "vixcloud.com", "vixcloud.net",
    "vidxgo.co", "vidxgo.to", "vidxgo.cc",
    "streamingcommunity", "streamingcommunity.app",
    "animeworld", "animeworld.ac", "animeworld.so",
    "animesaturn", "animesaturn.cx", "animesaturn.tv",
    "animeunity", "animeunity.so",
    "animepahe", "animepahe.pw",
    "vidxgo", "vidxgo.co",
    "vixsrc", "vixsrc.to", "vixsrc.net",
    # CDN generici
    "cloudflare.com", "cloudfront.net", "akamai.com",
    "fastly.net", "akamaized.net",
    # Estensioni video comuni
    "*.m3u8", "*.ts", "*.m4s", "*.mp4", "*.webm", "*.mkv",
]

# Blocca TUTTI i proxy per video
DISABLE_HLS_PROXY = True
DISABLE_DASH_PROXY = True
DISABLE_MPD_PROXY = True

# === CACHE SETTINGS ===
CACHE_TTL = 3600  # 1 ora per cataloghi
SEARCH_CACHE_TTL = 1800
META_CACHE_TTL = 86400  # 24h per meta

# === MEMORY LIMITS ===
MAX_MEMORY_MB = 512
CHROMIUM_MAX_MEMORY_MB = 256  # Limite per FlareSolverr Chromium

# === LOGGING ===
LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")  # Meno log = meno RAM

# === FLARSOLVERR CONFIG (solo per scraping) ===
FLARESOLVERR_URL = os.environ.get("FLARESOLVERR_URL", "http://127.0.0.1:8191")
FLARESOLVERR_PORT = 8191
FLARESOLVERR_HEADLESS = True
FLARESOLVERR_LOG_HTML = False
FLARESOLVERR_LOG_LEVEL = "ERROR"
FLARESOLVERR_CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-component-extensions-with-background-pages",
    "--disable-default-apps",
    "--disable-hang-monitor",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--disable-translate",
    "--metrics-recording-only",
    "--no-first-run",
    "--no-default-browser-check",
    "--no-pings",
    "--disable-background-mode",
    "--disable-features=TranslateUI,BlinkGenPropertyTrial",
    "--memory-pressure-off",
    "--max_old_space_size=256",  # Limite memoria Chromium
]

# === EXCLUDE DOMAINS FROM PROXY ===
# Tutti i domini video vengono esclusi dal proxy
PROXY_EXCLUDE_DOMAINS_EXTENDED = [
    # Video hosting
    "vix-content.net", "vixsrc.to", "vixsrc.net", "vixsrc.cc",
    "vixcloud.co", "vixcloud.com", "vixcloud.net",
    "vidxgo.co", "vidxgo.to", "vidxgo.cc",
    "streamingcommunity", "streamingcommunity.app",
    "animeworld", "animeworld.ac", "animeworld.so",
    "animesaturn", "animesaturn.cx", "animesaturn.tv",
    "animeunity", "animeunity.so",
    "animepahe", "animepahe.pw",
    "vidxgo", "vidxgo.co",
    "vixsrc", "vixsrc.to", "vixsrc.net",
    # CDN generici
    "cloudflare.com", "cloudfront.net", "akamai.com",
    "fastly.net", "akamaized.net",
    # Estensioni video
    "*.m3u8", "*.ts", "*.m4s", "*.mp4", "*.webm", "*.mkv",
]

# === DISABLE PROXY FEATURES ===
DISABLE_HLS_PROXY = True
DISABLE_DASH_PROXY = True
DISABLE_MPD_PROXY = True
DISABLE_SEGMENT_PROXY = True
DISABLE_EXTRACTOR_PROXY = True
DISABLE_RECORDING = True

# === CACHE SETTINGS ===
CACHE_TTL = 3600  # 1 ora per cataloghi
SEARCH_CACHE_TTL = 1800
META_CACHE_TTL = 86400  # 24h per meta
CATALOG_CACHE_TTL = 3600

# === MEMORY ===
MAX_MEMORY_MB = 512
CHROMIUM_MAX_MEMORY_MB = 256

# === LOGGING ===
LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")

# === FLARESOLVERR CONFIG ===
FLARESOLVERR_URL = os.environ.get("FLARESOLVERR_URL", "http://127.0.0.1:8191")
FLARESOLVERR_PORT = 8191
FLARESOLVERR_ENABLED = True
FLARESOLVERR_HEADLESS = True
FLARESOLVERR_LOG_HTML = False
FLARESOLVERR_LOG_LEVEL = "ERROR"
FLARESOLVERR_CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-component-extensions-with-background-pages",
    "--disable-default-apps",
    "--disable-hang-monitor",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--disable-translate",
    "--metrics-recording-only",
    "--no-first-run",
    "--no-default-browser-check",
    "--no-pings",
    "--disable-background-mode",
    "--disable-features=TranslateUI,BlinkGenPropertyTrial",
    "--memory-pressure-off",
    "--max_old_space_size=256",
]

# === DISABLE PROXY FEATURES ===
DISABLE_HLS_PROXY = True
DISABLE_DASH_PROXY = True
DISABLE_MPD_PROXY = True
DISABLE_SEGMENT_PROXY = True
DISABLE_EXTRACTOR_PROXY = True
DISABLE_RECORDING = True

# === CACHE SETTINGS ===
CACHE_TTL = 3600
SEARCH_CACHE_TTL = 1800
META_CACHE_TTL = 86400
CATALOG_CACHE_TTL = 3600

# === MEMORY ===
MAX_MEMORY_MB = 512
CHROMIUM_MAX_MEMORY_MB = 256

# === LOGGING ===
LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")

# === EXCLUDE DOMAINS FROM PROXY ===
PROXY_EXCLUDE_DOMAINS = [
    "vix-content.net", "vixsrc.to", "vixsrc.net", "vixsrc.cc",
    "vixcloud.co", "vixcloud.com", "vixcloud.net",
    "vidxgo.co", "vidxgo.to", "vidxgo.cc",
    "streamingcommunity", "streamingcommunity.app",
    "animeworld", "animeworld.ac", "animeworld.so",
    "animesaturn", "animesaturn.cx", "animesaturn.tv",
    "animeunity", "animeunity.so",
    "animepahe", "animepahe.pw",
    "vidxgo", "vidxgo.co",
    "vixsrc", "vixsrc.to", "vixsrc.net",
    "cloudflare.com", "cloudfront.net", "akamai.com",
    "fastly.net", "akamaized.net",
]

# Disable all proxy features
DISABLE_HLS_PROXY = True
DISABLE_DASH_PROXY = True
DISABLE_MPD_PROXY = True
DISABLE_SEGMENT_PROXY = True
DISABLE_EXTRACTOR_PROXY = True
DISABLE_RECORDING = True

# Cache settings
CACHE_TTL = 3600
SEARCH_CACHE_TTL = 1800
META_CACHE_TTL = 86400
CATALOG_CACHE_TTL = 3600

# Memory limits
MAX_MEMORY_MB = 512
CHROMIUM_MAX_MEMORY_MB = 256

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")

# FlareSolverr
FLARESOLVERR_URL = os.environ.get("FLARESOLVERR_URL", "http://127.0.0.1:8191")
FLARESOLVERR_PORT = 8191
FLARESOLVERR_ENABLED = True
FLARESOLVERR_HEADLESS = True
FLARESOLVERR_LOG_HTML = False
FLARESOLVERR_LOG_LEVEL = "ERROR"
FLARESOLVERR_CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-component-extensions-with-background-pages",
    "--disable-default-apps",
    "--disable-hang-monitor",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--disable-translate",
    "--metrics-recording-only",
    "--no-first-run",
    "--no-default-browser-check",
    "--no-pings",
    "--disable-background-mode",
    "--disable-features=TranslateUI,BlinkGenPropertyTrial",
    "--memory-pressure-off",
    "--max_old_space_size=256",
]