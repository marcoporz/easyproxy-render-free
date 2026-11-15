"""
Configure routes - Pagina di configurazione web per l'addon.
Mostra solo l'URL del manifest da inserire in Easy Streams.
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
    """Genera pagina HTML di configurazione per Easy Streams."""
    html = """
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EasyProxy Manifest-Only - Configurazione per Easy Streams</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #000000; --surface: #141414; --surface-2: #1f1f1f;
      --border: rgba(255,255,255,0.10); --border-strong: rgba(255,255,255,0.25);
      --text: #ffffff; --text-dim: #d4d4d4; --text-faint: #808080;
      --red: #e50914; --red-hover: #f6121d; --red-dim: #b81d24;
      --green: #22c55e; --green-dim: #16a34a;
    }
    * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif; background: var(--bg); color: var(--text); letter-spacing: -0.005em; }
    .mono { font-family: 'JetBrains Mono', ui-monospace, monospace; }
    .bg-fx { position: fixed; inset: 0; z-index: -1; pointer-events: none; overflow: hidden; background: #000; }
    .bg-fx::before { content: ''; position: absolute; top: -20%; left: -10%; right: -10%; height: 70%; background: radial-gradient(50% 60% at 20% 30%, rgba(229,9,20,0.18) 0%, transparent 60%), radial-gradient(50% 60% at 80% 20%, rgba(229,9,20,0.10) 0%, transparent 60%); filter: blur(20px); }
    .bg-fx::after { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%); }
    .card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; }
    .card:hover { border-color: var(--border-strong); }
    .btn-primary { background: var(--red); color: var(--text); transition: background 0.15s, transform 0.05s; font-weight: 700; letter-spacing: 0.02em; }
    .btn-primary:hover { background: #f6121d; } .btn-primary:active { transform: scale(0.98); }
    .btn-ghost { background: rgba(109,109,110,0.7); color: var(--text); border: none; font-weight: 600; transition: background 0.15s; }
    .btn-ghost:hover { background: rgba(109,109,110,0.4); }
    input::placeholder { color: var(--text-faint); } input { color: var(--text); }
    .input { background: #333; border: 1px solid transparent; transition: border-color 0.15s, background 0.15s; width: 100%; }
    .input:focus { outline: none; background: #454545; border-color: var(--red); }
    .section-bar { display: inline-block; width: 4px; height: 28px; background: var(--red); margin-right: 14px; vertical-align: middle; border-radius: 2px; }
    .fade-in { animation: fadeIn 0.4s ease-out; } @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    .copy-btn { background: var(--surface-2); border: 1px solid var(--border); color: var(--text-dim); font-size: 12px; padding: 6px 12px; border-radius: 4px; cursor: pointer; transition: all 0.15s; }
    .copy-btn:hover { background: var(--red); border-color: var(--red); color: var(--text); }
    .copy-btn.copied { background: var(--green); border-color: var(--green); color: var(--text); }
    .url-display { background: #0a0a0a; border: 1px solid var(--border); border-radius: 4px; padding: 12px; font-size: 13px; word-break: break-all; position: relative; }
    .label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; color: var(--text-faint); margin-bottom: 6px; display: block; }
    .optional-badge { font-size: 10px; background: rgba(255,255,255,0.1); color: var(--text-faint); padding: 2px 6px; border-radius: 3px; margin-left: 8px; }
    .step { display: flex; align-items: flex-start; gap: 12px; padding: 16px 0; border-bottom: 1px solid var(--border); }
    .step:last-child { border-bottom: none; }
    .step-num { width: 28px; height: 28px; background: var(--red); color: var(--text); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
    .step-content { flex: 1; }
    .step-title { font-weight: 600; margin-bottom: 4px; }
    .step-desc { color: var(--text-dim); font-size: 14px; line-height: 1.5; }
    .success-box { background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); border-radius: 6px; padding: 16px; margin-top: 16px; }
    .success-box h4 { color: var(--green); margin-bottom: 8px; }
    .success-box code { background: #0a0a0a; padding: 2px 6px; border-radius: 3px; font-size: 13px; }
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

  <main class="max-w-3xl mx-auto px-4 sm:px-6 py-12">
    <header class="text-center mb-12">
      <div class="flex flex-wrap items-center justify-center gap-2 mb-5">
        <div class="trust-badge"><span class="dot"></span> 100% gratis · Open source · Privacy first</div>
      </div>
      <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight mb-5 leading-[1.02]" style="letter-spacing:-0.035em;">
        EasyProxy Manifest-Only
      </h1>
      <p class="text-zinc-300 text-base sm:text-lg md:text-xl leading-relaxed mb-6 max-w-xl mx-auto">
        Solo manifest/catalog/meta. NESSUN proxy video. Stream diretti dai CDN.
        <br><span class="text-zinc-500">Questa pagina genera l'URL da inserire in <strong>Easy Streams</strong> (non installa direttamente su Stremio).</span>
      </p>
    </header>

    <section class="py-6 border-t border-white/[0.06] mb-8">
      <h2 class="text-2xl sm:text-3xl font-extrabold mb-6 flex items-center">
        <span class="section-bar"></span>
        Configurazione per Easy Streams
      </h2>
      
      <div class="card p-4 sm:p-6 mb-6">
        <div class="step">
          <div class="step-num">1</div>
          <div class="step-content">
            <div class="step-title">Inserisci l'URL pubblico del tuo servizio Render</div>
            <div class="step-desc">Es: <code class="mono text-xs bg-black/30 px-2 py-1 rounded">https://mio-easyproxy.onrender.com</code></div>
            <div class="mt-3">
              <span class="label">URL Pubblico Render</span>
              <input id="pub-host" type="text" autocomplete="off" spellcheck="false"
                class="input mono rounded-lg px-3.5 py-2.5 text-sm"
                placeholder="https://mio-servizio.onrender.com" />
            </div>
          </div>
        </div>
        
        <div class="step">
          <div class="step-num">2</div>
          <div class="step-content">
            <div class="step-title">Real-Debrid Token <span class="optional-badge">opzionale</span></div>
            <div class="step-desc">Per accedere a fonti premium (4K, cached torrents). Lascia vuoto per soli stream HTTP diretti.</div>
            <div class="mt-3">
              <span class="label">Real-Debrid API Token</span>
              <input id="rd-token" type="password" autocomplete="off" spellcheck="false"
                class="input mono rounded-lg px-3.5 py-2.5 text-sm"
                placeholder="Incolla qui il tuo token Real-Debrid (opzionale)" />
            </div>
          </div>
        </div>
        
        <div class="step">
          <div class="step-num">3</div>
          <div class="step-content">
            <div class="step-title">API Password <span class="optional-badge">opzionale</span></div>
            <div class="step-desc">Password per proteggere l'endpoint manifest (consigliato se l'URL è pubblico).</div>
            <div class="mt-3">
              <span class="label">API Password</span>
              <input id="api-password" type="password" autocomplete="off" spellcheck="false"
                class="input mono rounded-lg px-3.5 py-2.5 text-sm"
                placeholder="Imposta una password (opzionale)" />
            </div>
          </div>
        </div>
      </div>

      <button id="generate-btn" class="btn-primary w-full py-3.5 rounded text-base uppercase mb-6">▶ Genera URL Manifest</button>
      <p class="text-xs text-zinc-500 text-center mb-8">Stream HTTP diretti: AnimeWorld, AnimeSaturn, GuardaSerie, StreamingCommunity, CB01, Altadefinizione. Con Real-Debrid: torrent cached, 4K, fonti premium.</p>
    </section>

    <!-- RISULTATO -->
    <section id="result-card" class="card p-4 sm:p-6 mb-10 hidden fade-in">
      <div class="flex items-center gap-2 mb-4">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-green-400"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h3 class="text-base font-semibold text-zinc-100">URL Manifest per Easy Streams</h3>
      </div>
      <p class="text-sm text-zinc-400 mb-4">Copia questo URL e incollalo in <strong>Easy Streams → Settings → Proxy URL</strong></p>
      
      <div class="url-display mb-4">
        <span id="manifest-url" class="mono text-xs text-zinc-300 break-all">—</span>
        <button id="copy-url" class="copy-btn absolute right-3 top-3" style="top: 12px; right: 12px;">Copia</button>
      </div>
      
      <div class="grid sm:grid-cols-2 gap-3 mb-4">
        <button id="copy-url-btn" class="btn-ghost w-full px-5 py-2.5 rounded text-sm">📋 Copia URL Manifest</button>
        <button id="regenerate-btn" class="btn-ghost w-full px-5 py-2.5 rounded text-sm">← Nuova configurazione</button>
      </div>

      <div class="success-box">
        <h4>✅ Come usare in Easy Streams</h4>
        <ol class="text-sm text-zinc-300 space-y-2 list-decimal list-inside">
          <li>Apri Stremio → Addons → <strong>Easy Streams</strong> → Configure (icona ingranaggio)</li>
          <li>Incolla l'URL sopra in <strong>"Proxy URL"</strong> (o "Manifest URL" nelle versioni nuove)</li>
          <li>Se hai messo API Password, inseriscila in <strong>"Proxy Password"</strong></li>
          <li>Se hai messo Real-Debrid Token, Easy Streams lo userà automaticamente per fonti premium</li>
          <li>Salva e cerca film/serie: vedrai stream "DUAL" (4K video + audio ITA sincronizzato)</li>
        </ol>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="py-8 border-t border-white/[0.06] text-center text-xs text-zinc-500">
      <p>EasyProxy Manifest-Only · Open source · MIT</p>
      <p class="mt-1"><a href="https://github.com/realbestia1/EasyProxy" target="_blank" rel="noopener" class="hover:text-white">GitHub</a></p>
    </footer>
  </main>

  <script>
    function copyText(text, btn) { 
      navigator.clipboard.writeText(text).then(()=>{ 
        const o = btn.textContent; 
        btn.textContent = 'Copiato!'; 
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = o; btn.classList.remove('copied'); }, 1500); 
      }).catch(() => { btn.textContent = 'Errore'; setTimeout(() => btn.textContent = 'Copia', 1500); }); 
    }

    document.getElementById('generate-btn').addEventListener('click', () => {
      const pubHost = document.getElementById('pub-host').value.trim();
      if (!pubHost) { alert('Inserisci URL pubblico Render'); return; }
      
      const rdToken = document.getElementById('rd-token').value.trim();
      const apiPassword = document.getElementById('api-password').value.trim();
      
      // Build config object
      const config = { pub: pubHost };
      if (rdToken) config.rd = rdToken;
      if (apiPassword) config.pwd = apiPassword;
      
      const b64 = btoa(JSON.stringify(config));
      const base = window.location.origin;
      const manifestUrl = base + '/' + b64 + '/manifest.json';
      
      document.getElementById('manifest-url').textContent = manifestUrl;
      document.getElementById('result-card').classList.remove('hidden');
      document.getElementById('result-card').classList.add('fade-in');
      
      // Scroll to result
      document.getElementById('result-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    
    document.getElementById('copy-url-btn').addEventListener('click', () => {
      const url = document.getElementById('manifest-url').textContent;
      if (url && url !== '—') copyText(url, document.getElementById('copy-url-btn'));
    });
    
    document.getElementById('copy-url').addEventListener('click', () => {
      const url = document.getElementById('manifest-url').textContent;
      if (url && url !== '—') copyText(url, document.getElementById('copy-url'));
    });
    
    document.getElementById('regenerate-btn').addEventListener('click', () => { 
      document.getElementById('result-card').classList.add('hidden'); 
      document.getElementById('pub-host').value = '';
      document.getElementById('rd-token').value = '';
      document.getElementById('api-password').value = '';
      window.scrollTo({ top: document.querySelector('section').offsetTop - 80, behavior: 'smooth' }); 
    });
    
    // Enter key support
    ['pub-host', 'rd-token', 'api-password'].forEach(id => {
      document.getElementById(id).addEventListener('keydown', (e) => {
        if (e.key === 'Enter') document.getElementById('generate-btn').click();
      });
    });
  </script>
</body>
</html>"""
    return html