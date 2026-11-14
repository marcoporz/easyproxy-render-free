"""
Configure routes - Pagina di configurazione web per l'addon.
"""
import logging
import os
from aiohttp import web

logger = logging.getLogger(__name__)


def setup_configure_routes(app):
    """Registra route per configurazione."""
    
    async def configure_handler(request):
        """Pagina di configurazione HTML."""
        html = await _render_configure_page()
        return web.Response(text=html, content_type="text/html")
    
    app.router.add_get("/configure", configure_handler)
    app.router.add_get("/configure-en", configure_handler)


async def _render_configure_page() -> str:
    """Genera pagina HTML di configurazione."""
    # Legge template HTML da file o genera inline
    html = """
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EasyProxy Manifest-Only - Configurazione</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Bebas+Neue&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #000000; --surface: #141414; --surface-2: #1f1f1f;
      --border: rgba(255,255,255,0.10); --border-strong: rgba(255,255,255,0.25);
      --text: #ffffff; --text-dim: #d4d4d4; --text-faint: #808080;
      --red: #e50914; --red-hover: #f6121d; --red-dim: #b81d24;
    }
    * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif; background: var(--bg); color: var(--text); letter-spacing: -0.005em; }
    .mono { font-family: 'JetBrains Mono', ui-monospace, monospace; }
    .bg-fx { position: fixed; inset: 0; z-index: -1; pointer-events: none; overflow: hidden; background: #000; }
    .bg-fx::before { content: ''; position: absolute; top: -20%; left: -10%; right: -10%; height: 70%; background: radial-gradient(50% 60% at 20% 30%, rgba(229,9,20,0.18) 0%, transparent 60%), radial-gradient(50% 60% at 80% 20%, rgba(229,9,20,0.10) 0%, transparent 60%); filter: blur(20px); }
    .bg-fx::after { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%); }
    .card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; }
    .card:hover { border-color: var(--border-strong); }
    .stat-num { color: var(--text); font-feature-settings: "tnum" 1; }
    .stat-label { color: var(--text-faint); text-transform: uppercase; font-size: 11px; letter-spacing: 0.08em; font-weight: 600; }
    .btn-primary { background: var(--red); color: var(--text); transition: background 0.15s, transform 0.05s; font-weight: 700; letter-spacing: 0.02em; }
    .btn-primary:hover { background: #f6121d; } .btn-primary:active { transform: scale(0.98); }
    .btn-stremio { background: var(--red); color: var(--text); border: none; font-weight: 700; letter-spacing: 0.02em; transition: background 0.15s, transform 0.05s; }
    .btn-stremio:hover { background: #f6121d; } .btn-stremio:active { transform: scale(0.98); }
    .btn-ghost { background: rgba(109,109,110,0.7); color: var(--text); border: none; font-weight: 600; transition: background 0.15s; }
    .btn-ghost:hover { background: rgba(109,109,110,0.4); }
    input::placeholder { color: var(--text-faint); } input { color: var(--text); }
    .input { background: #333; border: 1px solid transparent; transition: border-color 0.15s, background 0.15s; }
    .input:focus { outline: none; background: #454545; border-color: var(--red); }
    .section-bar { display: inline-block; width: 4px; height: 28px; background: var(--red); margin-right: 14px; vertical-align: middle; border-radius: 2px; }
    .pulse-dot { animation: pulse 2.4s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
    .fade-in { animation: fadeIn 0.4s ease-out; } @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    .valid-badge { position: absolute; right: 88px; top: 50%; transform: translateY(-50%); display: flex; align-items: center; gap: 6px; font-size: 12px; padding: 4px 10px; border-radius: 6px; pointer-events: none; }
    .valid-badge.ok { background: rgba(34,197,94,0.12); color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }
    .valid-badge.err { background: rgba(239,68,68,0.12); color: #f87171; border: 1px solid rgba(239,68,68,0.25); }
    .valid-badge.loading { background: rgba(255,255,255,0.06); color: var(--text-dim); border: 1px solid var(--border); }
    .spinner { width: 10px; height: 10px; border: 1.5px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    ::selection { background: rgba(229,9,20,0.4); }
  </style>
</head>
<body class="min-h-screen">
  <div class="bg-fx" aria-hidden="true"></div>
  <nav class="border-b border-white/[0.06]">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <span class="mono text-[10px] text-zinc-600 hidden md:inline">Manifest-Only</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="trust-badge"><span class="dot"></span> Online</span>
        <a href="https://github.com/realbestia1/EasyProxy" target="_blank" rel="noopener" class="text-xs text-zinc-400 hover:text-white transition flex items-center gap-1.5">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.57.1.78-.25.78-.55v-2.13c-3.2.7-3.87-1.36-3.87-1.36-.52-1.34-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.12 3.05.74.81 1.18 1.84 1.18 3.1 0 4.42-2.69 5.4-5.25 5.69.41.36.78 1.07.78 2.15v3.19c0 .31.21.66.79.55C20.21 21.39 23.5 17.08 23.5 12 23.5 5.65 18.35.5 12 .5z"/></svg>
          GitHub
        </a>
      </div>
    </div>
  </nav>

  <main class="max-w-6xl mx-auto px-4 sm:px-6">
    <header class="pt-8 pb-12 md:pt-16 md:pb-20">
      <div class="text-center lg:text-left">
        <div class="flex flex-wrap items-center justify-center lg:justify-start gap-2 mb-5 md:mb-6">
          <div class="trust-badge"><span class="dot"></span> 100% gratis · Open source · Privacy first</div>
        </div>
        <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight mb-5 md:mb-6 leading-[1.02]" style="letter-spacing:-0.035em;">
          EasyProxy Manifest-Only
        </h1>
        <p class="text-zinc-300 text-base sm:text-lg md:text-xl leading-relaxed mb-6 md:mb-8 max-w-xl mx-auto lg:mx-0">
          Solo manifest/catalog/meta. NESSUN proxy video. Stream diretti dai CDN.
        </p>
        <div class="flex flex-wrap items-center justify-center lg:justify-start gap-3">
          <a href="#setup" class="btn-primary inline-flex items-center gap-2 px-7 py-3.5 rounded uppercase text-base">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            Configura
          </a>
        </div>
      </div>
    </header>

    <section id="setup" class="py-10 md:py-16 border-t border-white/[0.06] max-w-2xl mx-auto">
      <h2 class="text-2xl sm:text-3xl md:text-4xl font-extrabold mb-3 flex items-center justify-center md:justify-start">
        <span class="section-bar"></span>
        Configura il tuo link
      </h2>
      <p class="text-zinc-400 text-base sm:text-lg mb-8 md:mb-10 md:ml-[18px] text-center md:text-left">
        EasyProxy Manifest-Only funziona <strong class="text-white">senza Real-Debrid</strong> — solo stream HTTP diretti dai CDN.
      </p>

      <!-- Configurazione semplice -->
      <div class="card p-4 sm:p-6 mb-3">
        <div class="flex items-center gap-3 mb-4">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded bg-white/5 border border-white/10 flex items-center justify-center font-bold text-xs text-white">⚙</div>
            <div>
              <div class="font-semibold text-zinc-100">EasyProxy Manifest-Only</div>
              <div class="text-xs text-zinc-500">Solo manifest/catalog/meta - NESSUN proxy video</div>
            </div>
          </div>
        </div>
        <div class="relative">
          <input id="pub-host" type="text" autocomplete="off" spellcheck="false"
            class="input mono w-full rounded-lg px-3.5 py-2.5 pr-20 text-sm"
            placeholder="URL pubblico Render (es. https://mio-easyproxy.onrender.com)" />
        </div>
        <div class="mt-3 text-xs text-zinc-400">L'URL pubblico del tuo servizio Render (es. https://mio-easyproxy.onrender.com)</div>
      </div>

      <button id="generate-btn" class="btn-primary w-full py-3.5 rounded text-base uppercase">▶ Genera link</button>
      <p class="text-xs text-zinc-500 mt-3 text-center">Solo stream HTTP diretti (AnimeWorld, AnimeSaturn, GuardaSerie, StreamingCommunity). Niente Real-Debrid, niente proxy video.</    </p>
    </section>

    <!-- RISULTATO -->
    <section id="install-card" class="card p-4 sm:p-6 mb-10 hidden fade-in max-w-2xl mx-auto">
      <div class="flex items-center gap-2 mb-1">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-emerald-400"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h3 class="text-base font-semibold text-zinc-100">Link generato</h3>
      </div>
      <p class="text-sm text-zinc-400 mb-5">Solo stream HTTP diretti. Niente Real-Debrid, niente proxy video.</    </p>

      <a id="install-stremio" href="#" class="btn-stremio block text-center w-full px-5 py-3.5 rounded uppercase mb-2">
        <span class="inline-flex items-center gap-2 justify-center">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          Installa EasyProxy Manifest-Only
        </span>
      </a>
      <button id="copy-url" class="btn-ghost w-full px-5 py-2.5 rounded text-sm mb-6">Copia link manuale</button>

      <!-- QR -->
      <div class="grid md:grid-cols-[auto,1fr] gap-5 mb-6 items-center pt-2">
        <div class="flex justify-center"><div id="qr-code" class="inline-block bg-white p-2.5 rounded-lg"></div></div>
        <div>
          <div class="text-sm font-semibold text-zinc-100 mb-1.5">Mobile / Android TV</div>
          <p class="text-xs text-zinc-400 leading-relaxed">Inquadra il QR o copia il link. Apre Stremio direttamente.</p>
        </div>
      </div>
      <div class="mono text-xs text-zinc-500 bg-black/40 rounded-md px-3 py-2.5 border border-white/[0.06] break-all mb-5" id="install-url">—</div>
      <div class="text-center"><button id="regenerate-btn" class="btn-ghost px-5 py-2 rounded text-sm">← Nuovo link</button></div>
    </section>

    <!-- FOOTER -->
    <footer class="py-8 border-t border-white/[0.06] text-center text-xs text-zinc-500">
      <p>EasyProxy Manifest-Only · Open source · MIT</p>
      <p class="mt-1"><a href="https://github.com/realbestia1/EasyProxy" target="_blank" rel="noopener" class="hover:text-white">GitHub</a></p>
    </footer>
  </main>

  <script>
    function escapeHtml(s) { return String(s).replace(/&/g,'&').replace(/</g,'<').replace(/>/g,'>').replace(/"/g,'"'); }
    function copyText(text, btn) { navigator.clipboard.writeText(text).then(()=>{ const o=btn.textContent; btn.textContent='Copiato!'; setTimeout(()=>btn.textContent=o,1500); }); }
    function escapeHtml(s) { return String(s).replace(/&/g,'&').replace(/</g,'<').replace(/>/g,'>').replace(/"/g,'"'); }

    document.getElementById('generate-btn').addEventListener('click',()=>{
      const pubHost = document.getElementById('pub-host').value.trim();
      if(!pubHost){ alert('Inserisci URL pubblico Render'); return; }
      const b64 = btoa(JSON.stringify({pub: pubHost}));
      const base = window.location.origin;
      const manifestUrl = base + '/' + b64 + '/manifest.json';
      document.getElementById('install-stremio').href = 'stremio://' + encodeURIComponent(manifestUrl);
      document.getElementById('install-url').textContent = manifestUrl;
      new QRCode(document.getElementById('qr-code'),{text:manifestUrl,width:180,height:180,colorDark:'#000',colorLight:'#fff',correctLevel:QRCode.CorrectLevel.M});
      document.getElementById('install-card').classList.remove('hidden');
      document.getElementById('install-card').classList.add('fade-in');
      document.getElementById('install-url').textContent = manifestUrl;
    });
    document.getElementById('copy-url').onclick=()=>navigator.clipboard.writeText(document.getElementById('install-url').textContent).then(()=>{ const btn=document.getElementById('copy-url'); btn.textContent='Copiato!'; setTimeout(()=>btn.textContent='Copia link manuale',1500); });
    document.getElementById('regenerate-btn').addEventListener('click',()=>{ document.getElementById('install-card').classList.add('hidden'); window.scrollTo({top:document.getElementById('setup').offsetTop-80,behavior:'smooth'}); });
    new QRCode(document.getElementById('qr-code'),{text:'',width:180,height:180,colorDark:'#000',colorLight:'#fff',correctLevel:QRCode.CorrectLevel.M});
  </script>
</body>
</html>"""
    return html