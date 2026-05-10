import logging
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("finlancer-agency")

class OutputManager:
    def __init__(self, base_dir: str = "output"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_run_dir(self, run_id: str) -> Path:
        return self.base_dir / run_id

    def save_full_package(self, outputs: dict, run_id: str = None) -> dict[str, Path]:
        run_id = run_id or datetime.now().strftime("%Y-%m-%d")
        saved: dict[str, Path] = {}
        mapping = {
            "instagram_legenda":          ("instagram", "legendas.md"),
            "instagram_carrossel_textos": ("instagram", "carrossel_textos.md"),
            "instagram_engagement":       ("instagram", "engagement_dicas.md"),
            "tiktok_legenda":             ("tiktok",    "legenda_video.md"),
            "tiktok_engagement":          ("tiktok",    "engagement_dicas.md"),
            "tiktok_video_ideia":         ("tiktok",    "video_ideia.md"),
            "youtube_legenda":            ("youtube",   "titulo_descricao.md"),
            "youtube_engagement":         ("youtube",   "engagement_dicas.md"),
            "facebook_legenda":           ("facebook",  "legenda_video.md"),
            "facebook_storytelling":      ("facebook",  "storytelling.md"),
            "facebook_engagement":        ("facebook",  "engagement_dicas.md"),
            "video_master":               ("03_ugc_video", "01_briefing_geral.md"),
            "briefing_producao":          ("03_ugc_video", "02_diretrizes_producao.md"),
            "cenas_detalhadas":           ("03_ugc_video", "03_roteiro_cenas.md"),
            "narracao_completa":          ("03_ugc_video", "04_narracao_completa.md"),
            "overlay_plataforma":         ("03_ugc_video", "05_textos_overlay.md"),
            "trilha_sonora":              ("03_ugc_video", "06_trilha_sonora.md"),
            "visual_concept":             ("visual-conceito", "conceito.md"),
        }
        
        run_dir = self._get_run_dir(run_id)
        
        for key, (plat, filename) in mapping.items():
            content = outputs.get(key, "")
            if content:
                # Check if it's a string with enough content or a dict
                is_valid = False
                if isinstance(content, str) and len(content.strip()) > 20:
                    is_valid = True
                elif isinstance(content, dict):
                    is_valid = True
                
                if is_valid:
                    path = run_dir / plat / filename
                    path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if isinstance(content, dict):
                        content_str = json.dumps(content, indent=2, ensure_ascii=False)
                    else:
                        content_str = str(content)
                        
                    path.write_text(content_str, encoding="utf-8")
                    saved[key] = path
                else:
                    logger.warning(f"[{key}] ignorado — conteúdo muito curto ou inválido")
        
        return saved

    def save_ugc_narration(self, narration_script: str, run_id: str = None) -> Path:
        run_id = run_id or datetime.now().strftime("%Y-%m-%d")
        run_dir = self._get_run_dir(run_id)
        path = run_dir / "03_ugc_video" / "narracao-edicao.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        content = (
            "# Narração UGC — para edição de vídeo\n\n"
            "_Adicione este áudio em off e estas legendas durante a montagem dos clipes._\n\n"
            + narration_script
        )
        path.write_text(content, encoding="utf-8")
        return path
