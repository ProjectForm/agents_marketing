"""
╔══════════════════════════════════════════════════════════════╗
║   FINLANCER PUBLISHER — Fase 9 do agents_marketing           ║
║   Dashboard de aprovação + publicação Meta API               ║
╚══════════════════════════════════════════════════════════════╝

USO:
  # Aprovar e publicar o output mais recente
  python publish.py

  # Aprovar e publicar um output específico
  python publish.py --run 2026-05-14_060000

  # Só mostrar o que foi gerado (sem publicar)
  python publish.py --preview

  # Publicar direto sem dashboard (modo automático)
  python publish.py --auto --run 2026-05-14_060000
"""

import os
import sys
import json
import time
import argparse
import requests
import threading
import webbrowser
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv
load_dotenv()

# ──────────────────────────────────────────────
# CONFIGURAÇÃO
# ──────────────────────────────────────────────

class Config:
    ACCESS_TOKEN  = os.getenv("META_ACCESS_TOKEN", "")
    PAGE_ID       = os.getenv("FACEBOOK_PAGE_ID", "")
    IG_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")
    API_VERSION   = os.getenv("META_API_VERSION", "v21.0")
    BASE_URL      = f"https://graph.facebook.com/{API_VERSION}"
    OUTPUT_DIR    = Path(__file__).parent / "output"
    PORT          = 8765  # porta do dashboard local

    @classmethod
    def validate(cls):
        missing = [k for k, v in {
            "META_ACCESS_TOKEN": cls.ACCESS_TOKEN,
            "FACEBOOK_PAGE_ID": cls.PAGE_ID,
            "INSTAGRAM_BUSINESS_ACCOUNT_ID": cls.IG_ACCOUNT_ID,
        }.items() if not v]
        if missing:
            raise ValueError(f"❌ Faltando no .env: {', '.join(missing)}")


# ──────────────────────────────────────────────
# META API CLIENT
# ──────────────────────────────────────────────

class MetaClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.params = {"access_token": Config.ACCESS_TOKEN}

    def post(self, endpoint, data):
        r = self.session.post(f"{Config.BASE_URL}/{endpoint}", data=data)
        d = r.json()
        if "error" in d:
            raise RuntimeError(f"Meta API: {d['error']['message']}")
        return d

    def get(self, endpoint, params=None):
        r = self.session.get(f"{Config.BASE_URL}/{endpoint}", params=params or {})
        d = r.json()
        if "error" in d:
            raise RuntimeError(f"Meta API: {d['error']['message']}")
        return d


# ──────────────────────────────────────────────
# LEITOR DE OUTPUTS
# ──────────────────────────────────────────────

def find_latest_run():
    """Encontra o run_id mais recente na pasta output/."""
    runs = [d for d in Config.OUTPUT_DIR.iterdir()
            if d.is_dir() and not d.name.startswith("test")]
    if not runs:
        raise FileNotFoundError("Nenhum output encontrado em output/")
    return sorted(runs, key=lambda x: x.name)[-1].name


def load_run_content(run_id: str) -> dict:
    """Carrega todo o conteúdo gerado de um run_id."""
    base = Config.OUTPUT_DIR / run_id
    if not base.exists():
        raise FileNotFoundError(f"Run não encontrado: {run_id}")

    def read(path):
        p = base / path
        if p.exists():
            text = p.read_text(encoding="utf-8")
            # Remove o header de aprovação automática
            if text.startswith("<!-- Aprovado"):
                text = text.split("-->", 1)[-1].strip()
            return text
        return ""

    return {
        "run_id": run_id,
        "instagram": {
            "legenda":   read("instagram/legendas.md"),
            "carrossel": read("instagram/carrossel_textos.md"),
            "engagement": read("instagram/engagement_dicas.md"),
        },
        "facebook": {
            "legenda":      read("facebook/legenda_video.md"),
            "storytelling": read("facebook/storytelling.md"),
            "engagement":   read("facebook/engagement_dicas.md"),
        },
        "tiktok": {
            "legenda":   read("tiktok/legenda_video.md"),
            "video_ideia": read("tiktok/video_ideia.md"),
        },
        "video": {
            "roteiro":    read("03_ugc_video/03_roteiro_cenas.md"),
            "briefing":   read("03_ugc_video/01_briefing_geral.md"),
            "overlays":   read("03_ugc_video/05_textos_overlay.md"),
            "trilha":     read("03_ugc_video/06_trilha_sonora.md"),
        },
        "visual":   read("visual-conceito/conceito.md"),
        "revisao":  read("REVISAO-FINAL.md"),
    }


# ──────────────────────────────────────────────
# PUBLISHER
# ──────────────────────────────────────────────

class Publisher:
    def __init__(self):
        self.client = MetaClient()
        self.results = {}

    def publish_facebook(self, message: str) -> str:
        print("📘 Publicando no Facebook...")
        r = self.client.post(f"{Config.PAGE_ID}/feed", {"message": message})
        post_id = r["id"]
        print(f"   ✅ Facebook publicado! ID: {post_id}")
        return post_id

    def publish_facebook_with_image(self, message: str, image_url: str) -> str:
        print("📘 Publicando foto no Facebook...")
        r = self.client.post(f"{Config.PAGE_ID}/photos", {
            "url": image_url,
            "caption": message,
        })
        post_id = r.get("post_id") or r.get("id")
        print(f"   ✅ Facebook foto publicada! ID: {post_id}")
        return post_id

    def publish_instagram(self, caption: str, image_url: str) -> str:
        print("📸 Publicando no Instagram...")
        container = self.client.post(f"{Config.IG_ACCOUNT_ID}/media", {
            "image_url": image_url,
            "caption": caption,
        })
        cid = container["id"]
        # Aguarda processamento
        for _ in range(10):
            s = self.client.get(cid, {"fields": "status_code"})
            if s.get("status_code") == "FINISHED":
                break
            time.sleep(5)
        r = self.client.post(f"{Config.IG_ACCOUNT_ID}/media_publish", {"creation_id": cid})
        post_id = r["id"]
        print(f"   ✅ Instagram publicado! ID: {post_id}")
        return post_id

    def publish_approved(self, approved: dict, image_url: str = "") -> dict:
        """
        Publica apenas o que foi aprovado no dashboard.
        approved: dict com booleanos {facebook: True, instagram: True, ...}
        """
        results = {}

        if approved.get("facebook"):
            text = approved.get("facebook_text", "")
            if text:
                if image_url:
                    results["facebook"] = self.publish_facebook_with_image(text, image_url)
                else:
                    results["facebook"] = self.publish_facebook(text)

        if approved.get("instagram") and image_url:
            text = approved.get("instagram_text", "")
            if text:
                results["instagram"] = self.publish_instagram(text, image_url)

        # Salva log de publicação
        log_path = Config.OUTPUT_DIR / approved.get("run_id", "unknown") / "PUBLICADO.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_data = {
            "published_at": datetime.now().isoformat(),
            "results": results,
            "approved": approved,
        }
        log_path.write_text(json.dumps(log_data, ensure_ascii=False, indent=2))
        print(f"\n📄 Log salvo: {log_path}")

        return results


# ──────────────────────────────────────────────
# DASHBOARD WEB LOCAL
# ──────────────────────────────────────────────

# Estado global do servidor
_server_state = {
    "content": {},
    "approved": None,
    "done": False,
}


def build_html(content: dict) -> str:
    """Gera o HTML do dashboard de aprovação."""
    run_id = content.get("run_id", "")
    ig = content.get("instagram", {})
    fb = content.get("facebook", {})
    tt = content.get("tiktok", {})
    vd = content.get("video", {})
    rev = content.get("revisao", "")

    def card(title, icon, field_id, text, color="#10b981"):
        escaped = text.replace("`", "&#96;").replace("</", "<\\/")
        return f"""
        <div class="card" id="card-{field_id}">
            <div class="card-header">
                <span class="icon">{icon}</span>
                <span class="card-title">{title}</span>
                <label class="toggle-wrap">
                    <input type="checkbox" class="approve-cb" data-field="{field_id}" checked>
                    <span class="toggle-label">Aprovar</span>
                </label>
            </div>
            <textarea id="text-{field_id}" class="content-area">{text.replace('<', '&lt;').replace('>', '&gt;')}</textarea>
        </div>"""

    ig_card  = card("Instagram — Legenda Reel", "📸", "instagram", ig.get("legenda", ""))
    fb_card  = card("Facebook — Storytelling", "📘", "facebook", fb.get("storytelling", "") or fb.get("legenda", ""))
    tt_card  = card("TikTok — Legenda", "🎵", "tiktok", tt.get("legenda", ""))
    vd_card  = card("Roteiro UGC — Cenas", "🎬", "video_roteiro", vd.get("roteiro", ""))
    rev_card = card("Revisão do Brand Director", "✅", "revisao", rev)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Finlancer — Dashboard de Aprovação</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #0f172a; color: #f1f5f9; min-height: 100vh; }}
  .header {{ background: #1e293b; border-bottom: 1px solid #334155;
             padding: 16px 32px; display: flex; align-items: center;
             justify-content: space-between; position: sticky; top: 0; z-index: 100; }}
  .logo {{ display: flex; align-items: center; gap: 10px; }}
  .logo-dot {{ width: 10px; height: 10px; border-radius: 50%; background: #10b981; }}
  .logo-text {{ font-size: 18px; font-weight: 600; color: #f1f5f9; }}
  .run-badge {{ background: #0f172a; border: 1px solid #334155;
                padding: 4px 12px; border-radius: 20px;
                font-size: 12px; color: #94a3b8; }}
  .main {{ max-width: 900px; margin: 0 auto; padding: 24px 16px; }}
  .section-title {{ font-size: 13px; font-weight: 600; text-transform: uppercase;
                    letter-spacing: .08em; color: #64748b; margin: 24px 0 12px; }}
  .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px;
           overflow: hidden; margin-bottom: 16px; transition: border-color .2s; }}
  .card.rejected {{ border-color: #ef4444; opacity: .6; }}
  .card-header {{ display: flex; align-items: center; gap: 10px;
                  padding: 12px 16px; border-bottom: 1px solid #334155; }}
  .icon {{ font-size: 18px; }}
  .card-title {{ font-size: 14px; font-weight: 600; flex: 1; }}
  .toggle-wrap {{ display: flex; align-items: center; gap: 6px; cursor: pointer; }}
  .approve-cb {{ accent-color: #10b981; width: 16px; height: 16px; cursor: pointer; }}
  .toggle-label {{ font-size: 12px; color: #94a3b8; }}
  .content-area {{ width: 100%; background: transparent; border: none; outline: none;
                   color: #e2e8f0; font-family: inherit; font-size: 13px;
                   line-height: 1.6; padding: 14px 16px; resize: vertical;
                   min-height: 120px; max-height: 400px; }}
  .image-section {{ background: #1e293b; border: 1px solid #334155;
                    border-radius: 12px; padding: 16px; margin-bottom: 16px; }}
  .image-section label {{ font-size: 13px; color: #94a3b8; display: block; margin-bottom: 8px; }}
  .image-input {{ width: 100%; background: #0f172a; border: 1px solid #334155;
                  border-radius: 8px; padding: 10px 14px; color: #f1f5f9;
                  font-size: 13px; outline: none; }}
  .image-input:focus {{ border-color: #10b981; }}
  .actions {{ position: sticky; bottom: 0; background: #1e293b;
              border-top: 1px solid #334155; padding: 16px 32px;
              display: flex; gap: 12px; justify-content: flex-end;
              margin-top: 24px; border-radius: 0 0 12px 12px; }}
  .btn {{ padding: 10px 24px; border-radius: 8px; font-size: 14px;
          font-weight: 600; cursor: pointer; border: none; transition: all .2s; }}
  .btn-primary {{ background: #10b981; color: #fff; }}
  .btn-primary:hover {{ background: #059669; }}
  .btn-secondary {{ background: #334155; color: #94a3b8; }}
  .btn-secondary:hover {{ background: #475569; color: #f1f5f9; }}
  .status-bar {{ display: none; background: #064e3b; border: 1px solid #10b981;
                 border-radius: 8px; padding: 12px 16px; margin-top: 16px;
                 font-size: 13px; color: #6ee7b7; }}
  .status-bar.show {{ display: block; }}
  .meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  @media (max-width: 600px) {{ .meta-grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="header">
  <div class="logo">
    <div class="logo-dot"></div>
    <span class="logo-text">Finlancer Publisher</span>
  </div>
  <span class="run-badge">Run: {run_id}</span>
</div>

<div class="main">
  <p class="section-title">Revisão do Brand Director</p>
  {rev_card}

  <p class="section-title">Conteúdo para Redes Sociais</p>
  <div class="meta-grid">
    {ig_card}
    {fb_card}
  </div>
  {tt_card}

  <p class="section-title">Produção de Vídeo</p>
  {vd_card}

  <p class="section-title">Imagem para publicação (URL pública)</p>
  <div class="image-section">
    <label>Cole a URL da imagem hospedada (Cloudinary, Drive público, Imgur, etc.)</label>
    <input type="text" id="image-url" class="image-input"
           placeholder="https://res.cloudinary.com/seu-dominio/imagem.jpg">
  </div>

  <div id="status" class="status-bar"></div>
</div>

<div class="actions">
  <button class="btn btn-secondary" onclick="rejectAll()">Rejeitar tudo</button>
  <button class="btn btn-secondary" onclick="window.close()">Fechar</button>
  <button class="btn btn-primary" onclick="submitApproval()">
    🚀 Publicar aprovados
  </button>
</div>

<script>
  document.querySelectorAll('.approve-cb').forEach(cb => {{
    cb.addEventListener('change', function() {{
      const card = document.getElementById('card-' + this.dataset.field);
      card.classList.toggle('rejected', !this.checked);
    }});
  }});

  function rejectAll() {{
    document.querySelectorAll('.approve-cb').forEach(cb => {{
      cb.checked = false;
      const card = document.getElementById('card-' + cb.dataset.field);
      card.classList.add('rejected');
    }});
  }}

  function submitApproval() {{
    const payload = {{
      run_id: '{run_id}',
      image_url: document.getElementById('image-url').value.trim(),
    }};
    document.querySelectorAll('.approve-cb').forEach(cb => {{
      payload[cb.dataset.field] = cb.checked;
      if (cb.checked) {{
        const ta = document.getElementById('text-' + cb.dataset.field);
        payload[cb.dataset.field + '_text'] = ta ? ta.value : '';
      }}
    }});

    const status = document.getElementById('status');
    status.textContent = '⏳ Enviando para publicação...';
    status.classList.add('show');

    fetch('/approve', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify(payload)
    }})
    .then(r => r.json())
    .then(data => {{
      if (data.ok) {{
        status.textContent = '✅ Publicado com sucesso! ' + JSON.stringify(data.results);
        status.style.background = '#064e3b';
      }} else {{
        status.textContent = '❌ Erro: ' + data.error;
        status.style.background = '#450a0a';
      }}
    }})
    .catch(e => {{
      status.textContent = '❌ Erro de conexão: ' + e;
      status.style.background = '#450a0a';
    }});
  }}
</script>
</body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silencia logs do servidor

    def do_GET(self):
        if self.path == "/":
            html = build_html(_server_state["content"]).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/approve":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            approved = json.loads(body)
            _server_state["approved"] = approved
            _server_state["done"] = True

            try:
                Config.validate()
                publisher = Publisher()
                results = publisher.publish_approved(approved, approved.get("image_url", ""))
                resp = json.dumps({"ok": True, "results": results}).encode("utf-8")
            except Exception as e:
                resp = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)


def run_dashboard(content: dict):
    """Abre o dashboard no browser e aguarda aprovação."""
    _server_state["content"] = content
    _server_state["done"] = False

    server = HTTPServer(("localhost", Config.PORT), DashboardHandler)
    url = f"http://localhost:{Config.PORT}"
    print(f"\n🌐 Dashboard aberto em: {url}")
    print("   Revise o conteúdo, edite se quiser, e clique em 'Publicar aprovados'.")
    print("   Pressione Ctrl+C para cancelar.\n")

    # Abre o browser automaticamente
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    # Roda o servidor até receber a aprovação
    server.timeout = 1
    while not _server_state["done"]:
        server.handle_request()
    server.server_close()


# ──────────────────────────────────────────────
# PREVIEW NO TERMINAL
# ──────────────────────────────────────────────

def preview_content(content: dict):
    """Mostra resumo do conteúdo no terminal."""
    print("\n" + "="*60)
    print(f"  RUN: {content['run_id']}")
    print("="*60)

    ig = content.get("instagram", {})
    fb = content.get("facebook", {})

    if ig.get("legenda"):
        print("\n📸 INSTAGRAM — Legenda:")
        print(ig["legenda"][:300])

    if fb.get("storytelling"):
        print("\n📘 FACEBOOK — Início do Storytelling:")
        print(fb["storytelling"][:300] + "...")

    rev = content.get("revisao", "")
    if rev:
        status_line = [l for l in rev.split("\n") if "STATUS" in l.upper()]
        if status_line:
            print(f"\n✅ Brand Director: {status_line[0]}")

    print("\n" + "="*60)


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Finlancer Publisher — Dashboard de aprovação e publicação")
    parser.add_argument("--run",     help="Run ID específico (ex: 2026-05-14_060000)")
    parser.add_argument("--preview", action="store_true", help="Só mostra o conteúdo, não abre o dashboard")
    parser.add_argument("--auto",    action="store_true", help="Publica tudo sem dashboard (modo automático)")
    parser.add_argument("--image-url", help="URL da imagem para publicação automática")
    args = parser.parse_args()

    # Encontra o run
    run_id = args.run or find_latest_run()
    print(f"📂 Carregando run: {run_id}")

    content = load_run_content(run_id)

    if args.preview:
        preview_content(content)
        return

    if args.auto:
        # Modo automático: publica tudo sem dashboard
        Config.validate()
        publisher = Publisher()
        approved = {
            "run_id": run_id,
            "facebook": True,
            "facebook_text": content["facebook"].get("storytelling") or content["facebook"].get("legenda"),
            "instagram": bool(args.image_url),
            "instagram_text": content["instagram"].get("legenda"),
            "image_url": args.image_url or "",
        }
        results = publisher.publish_approved(approved, args.image_url or "")
        print(f"\n✅ Publicado: {results}")
        return

    # Modo padrão: abre o dashboard
    run_dashboard(content)


if __name__ == "__main__":
    main()
