# EasyProxy Manifest-Only per Render Free Tier

Versione **Manifest-Only** di EasyProxy ottimizzata per **Render Free Tier** (512MB RAM, 5GB bandwidth/mese).

## 🎯 Caratteristiche

- **Solo manifest/catalog/meta/search/configure** - NESSUN proxy video/segmenti
- **Zero bandwidth su Render** - Lo streaming avviene direttamente dai CDN al dispositivo
- **FlareSolverr solo per scraping Cloudflare** durante catalog/ricerca
- **Real-Debrid opzionale** - Configurabile via pagina `/configure`
- **Deploy su Render Free** - Porta 10000, 512MB RAM, build Docker

## 🚀 Deploy su Render

### Opzione 1: Deploy automatico (consigliato)

1. Fork questo repository
2. Vai su [Render Dashboard](https://dashboard.render.com)
3. Clicca "New" → "Web Service"
4. Connetti il repository GitHub
5. Render rileverà automaticamente `render.yaml` e configurerà tutto

### Opzione 2: Deploy manuale

1. Crea un nuovo Web Service su Render
2. Runtime: **Docker**
3. Build Command: `./build.sh`
4. Start Command: `./start.sh`
5. Plan: **Free**
6. Porta: **10000**
7. Health Check Path: `/health`

### Variabili d'ambiente (già in render.yaml)

```env
PORT=10000
LOG_LEVEL=WARNING
MANIFEST_ONLY=true
DISABLE_PROXY=true
DISABLE_HLS_PROXY=true
DISABLE_DASH_PROXY=true
DISABLE_RECORDING=true
FLARESOLVERR_URL=http://127.0.0.1:8191
```

## 🔧 Configurazione

Dopo il deploy, visita `https://tuo-servizio.onrender.com/configure` per:

1. Inserire l'URL pubblico del tuo servizio Render
2. Generare il link di installazione per Stremio
3. (Opzionale) Configurare Real-Debrid per fonti premium

## 📋 Endpoints

| Endpoint | Descrizione |
|----------|-------------|
| `/manifest.json` | Manifest Stremio |
| `/configure` | Pagina configurazione web |
| `/catalog/{id}.json` | Cataloghi (search, anime, etc.) |
| `/meta/{type}/{id}.json` | Metadati film/serie/anime |
| `/search?search=...` | Ricerca unificata |
| `/health` | Health check per Render |

## 🏗️ Sviluppo locale

```bash
# Installa dipendenze
pip install -r requirements.txt

# Avvia (senza FlareSolverr per test rapidi)
FLARESOLVERR_ENABLED=false python3 main.py

# Con FlareSolverr (richiede Chromium + Xvfb)
python3 main.py
```

## 📦 Struttura

```
easyproxy-render-free/
├── main.py                 # Entry point
├── config.py               # Configurazione
├── requirements.txt        # Dipendenze Python
├── Dockerfile              # Build Docker
├── start.sh                # Startup script
├── build.sh                # Build script per Render
├── render.yaml             # Config Render
├── routes/
│   ├── manifest.py         # /manifest.json
│   ├── catalog.py          # /catalog/*
│   ├── meta.py             # /meta/*
│   ├── search.py           # /search
│   ├── configure.py        # /configure
│   └── health.py           # /health
└── services/
    ├── flaresolverr.py     # FlareSolverr client
    └── scraper_manager.py  # Scraping cataloghi
```

## ⚡ Ottimizzazioni Render Free

- **RAM**: ~30-50MB base, <256MB con FlareSolverr
- **Bandwidth**: ~0MB (streaming diretto CDN→Client)
- **CPU**: Minimo (solo HTTP routing + scraping)
- **Cold start**: ~10-15s (FlareSolverr Chromium init)

## 🔒 Sicurezza

- Nessun token/segreto hardcoded
- Variabili d'ambiente per config
- CORS aperto per Stremio (necessario)
- FlareSolverr solo localhost (porta 8191)

## 📝 Licenza

MIT - Open Source