"""
Configure routes - Pagina di configurazione per Easy Streams.
Input: Render URL + API Password → Output: Manifest URL da incollare in Easy Streams.
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
  <title>EasyProxy - Configurazione per Easy Streams</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root { --bg:#000; --surface:#141414; --border:rgba(255,255,255,.1); --text:#fff; --text-dim:#d4d4d4; --text-faint:#808080; --red:#e50914; --green:#22c55e; }
    * { -webkit-font-smoothing:antialiased; }
    body { font-family:'Inter',system-ui,sans-serif; background:var(--bg); color:var(--text); letter-spacing:-.005em; }
    .mono { font-family:'JetBrains Mono',ui-monospace,monospace; }
    .card { background:var(--surface); border:1px solid var(--border); border-radius:8px; }
    .input { width:100%; background:#222; border:1px solid transparent; color:var(--text); padding:12px 14px; border-radius:6px; font-size:14px; transition:border-color .15s,background .15s; }
    .input:focus { outline:none; background:#333; border-color:var(--red); }
    .input::placeholder { color:var(--text-faint); }
    .btn { background:var(--red); color:var(--text); font-weight:700; padding:14px 24px; border-radius:6px; border:none; cursor:pointer; font-size:14px; transition:background .15s,transform .05s; }
    .btn:hover { background:#f6121d; } .btn:active { transform:scale(.98); }
    .btn:disabled { opacity:.5; cursor:not-allowed; }
    .btn-ghost { background:rgba(109,109,110,.7); }
    .btn-ghost:hover { background:rgba(109,109,110,.4); }
    .url-box { background:#0a0a0a; border:1px solid var(--border); border-radius:6px; padding:16px; font-size:13px; word-break:break-all; position:relative; min-height:60px; }
    .label { display:block; font-size:11px; text-transform:uppercase; letter-spacing:.08em; font-weight:600; color:var(--text-faint); margin-bottom:6px; }
    .copy-btn { position:absolute; right:12px; top:12px; background:var(--surface); border:1px solid var(--border); color:var(--text-dim); font-size:11px; padding:6px 10px; border-radius:4px; cursor:pointer; }
    .copy-btn:hover { background:var(--red); border-color:var(--red); color:var(--text); }
    .copy-btn.copied { background:var(--green); border-color:var(--green); color:#000; }
    .step { border-bottom:1px solid var(--border); padding:20px 0; }
    .step:last-child { border-bottom:none; }
    .step-title { font-weight:600; margin-bottom:4px; }
    .step-desc { color:var(--text-dim); font-size:14px; line-height:1.5; }
    .badge { font-size:10px; background:rgba(255,255,255,.1); color:var(--text-faint); padding:2px 6px; border-radius:3px; margin-left:8px; }
    .success { background:rgba(34,197,94,.1); border:1px solid rgba(34,197,94,.3); border-radius:6px; padding:16px; margin-top:16px; }
    .success h4 { color:var(--green); margin-bottom:8px; }
    .success code { background:#0a0a0a; padding:2px 6px; border-radius:3px; font-size:13px; }
  </style>
</head>
<body class="min-h-screen">
  <nav class="border-b border-white/5">
    <div class="max-w-2xl mx-auto px-4 py-4 flex items-center justify-between">
      <span class="mono text-[10px] text-zinc-600">EasyProxy Manifest-Only</span>
      <a href="https://github.com/realbestia1/EasyProxy" target="_blank" rel="noopener" class="text-xs text-zinc-400 hover:text-white flex items-center gap-1.5">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.57.1.78-.25.78-.55v-2.13c-3.2.7-3.87-1.36-3.87-1.36-.52-1.34-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.12 3.05.74.81 1.18 1.84 1.18 3.1 0 4.42-2.69 5.4-5.25 5.69.41.36.78 1.07.78 2.15v3.19c0 .31.21.66.79.55C20.21 21.39 23.5 17.08 23.5 12 23.5 5.65 18.35.5 12 .5z"/></svg>
        GitHub
      </a>
    </div>
  </nav>

  <main class="max-w-2xl mx-auto px-4 py-12">
    <header class="text-center mb-10">
      <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3" style="letter-spacing:-0.03em;">EasyProxy per Easy Streams</h1>
      <p class="text-zinc-400">Genera l'URL manifest da incollare in <strong>Easy Streams → Settings → Proxy URL</strong></p>
    </header>

    <section class="card p-6 mb-8">
      <h2 class="text-lg font-bold mb-4">Configurazione</h2>
      
      <div class="step">
        <div class="step-title">URL pubblico Render <span class="badge">richiesto</span></div>
        <div class="step-desc">L'URL del tuo servizio su Render (es. <code class="mono text-xs bg-black/30 px-2 py-1 rounded">https://mio-proxy.onrender.com</code>)</div>
        <label class="label">Render URL</label>
        <input id="render-url" type="url" class="input mono" placeholder="https://mio-servizio.onrender.com" value="https://easyproxy-render-free.onrender.com" />
      </div>

      <div class="step">
        <div class="step-title">API Password <span class="badge">opzionale</span></div>
        <div class="step-desc">Password per proteggere l'endpoint manifest. Stessa password va messa in Easy Streams → Proxy Password.</div>
        <label class="label">API Password</label>
        <input id="api-pwd" type="password" class="input mono" placeholder="Lascia vuoto se non serve" />
      </div>

      <button id="generate-btn" class="btn w-full mt-6">Genera URL Manifest</button>
    </section>

    <section id="result" class="card p-6 hidden">
      <h3 class="text-lg font-bold mb-3 flex items-center gap-2">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-green-400"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        URL Manifest per Easy Streams
      </h3>
      <p class="text-sm text-zinc-400 mb-4">Copia e incolla in <strong>Easy Streams → Settings → Proxy URL</strong></p>
      
      <div class="url-box mb-4">
        <span id="manifest-url" class="mono text-xs text-zinc-300 block">—</span>
        <button id="copy-btn" class="copy-btn">Copia</button>
      </div>
      
      <div class="flex gap-3 mb-6">
        <button id="copy-url-btn" class="btn-ghost flex-1 py-2.5 rounded">📋 Copia URL</button>
        <button id="reset-btn" class="btn-ghost flex-1 py-2.5 rounded">← Nuova configurazione</button>
      </div>

      <div class="success">
        <h4>Come usare in Easy Streams</h4>
        <ol class="text-sm text-zinc-300 space-y-2 list-decimal list-inside">
          <li>Apri Stremio → Addons → <strong>Easy Streams</strong> → Configure (icona ⚙️)</li>
          <li>Incolla l'URL sopra in <strong>"Proxy URL"</strong></li>
          <li>Se hai messo API Password, inseriscila in <strong>"Proxy Password"</strong></li>
          <li>Salva e cerca film/serie: vedrai stream con proxy attivo</li>
        </ol>
      </div>
    </section>

    <footer class="py-8 text-center text-xs text-zinc-500">
      <p>EasyProxy Manifest-Only · Open source · MIT</p>
    </footer>
  </main>

  <script>
    function copyText(text, btn) {
      navigator.clipboard.writeText(text).then(()=>{ 
        const o = btn.textContent; 
        btn.textContent = 'Copiato!'; 
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = o; btn.classList.remove('copied'); }, 1500); 
      });
    }

    document.getElementById('generate-btn').addEventListener('click', () => {
      const renderUrl = document.getElementById('render-url').value.trim();
      const apiPwd = document.getElementById('api-pwd').value.trim();
      if (!renderUrl) { alert('Inserisci URL Render'); return; }
      
      const config = { pub: renderUrl };
      if (apiPwd) config.pwd = apiPwd;
      
      const b64 = btoa(JSON.stringify(config)).replace(/=/g,'').replace(/\+/g,'-').replace(/\//g,'_');
      const manifestUrl = renderUrl.replace(/\/$/,'') + '/' + b64 + '/manifest.json';
      
      document.getElementById('manifest-url').textContent = manifestUrl;
      document.getElementById('result').classList.remove('hidden');
      document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
    });
    
    document.getElementById('copy-url-btn').addEventListener('click', () => 
      copyText(document.getElementById('manifest-url').textContent, document.getElementById('copy-url-btn'))
    );
    document.getElementById('copy-btn').addEventListener('click', () => 
      copyText(document.getElementById('manifest-url').textContent, document.getElementById('copy-btn'))
    );
    document.getElementById('reset-btn').addEventListener('click', () => { 
      document.getElementById('result').classList.add('hidden'); 
      document.getElementById('api-pwd').value = '';
      window.scrollTo({top:0,behavior:'smooth'}); 
    });
    
    ['render-url','api-pwd'].forEach(id => {
      document.getElementById(id).addEventListener('keydown', e => { if(e.key==='Enter') document.getElementById('generate-btn').click(); });
    });
  </script>
</body>
</html>"""
    return html