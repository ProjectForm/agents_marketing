import logging
import platform
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

BASE_OUTPUT = Path(__file__).parent.parent / "output"
PLATFORMS = ["instagram", "facebook", "tiktok", "youtube", "videos", "video-criativo"]


class OutputManager:
    """Saves agent outputs organized by date and platform — all as PDF files."""

    def __init__(self, base_dir: Path = BASE_OUTPUT):
        self.base_dir = base_dir

    def _get_run_dir(self, date_str: str = None) -> Path:
        date_str = date_str or datetime.now().strftime("%Y-%m-%d")
        run_dir = self.base_dir / date_str
        for platform in PLATFORMS:
            (run_dir / platform).mkdir(parents=True, exist_ok=True)
        (run_dir / "instagram" / "slides").mkdir(parents=True, exist_ok=True)
        return run_dir

    # ─── PDF generation ───────────────────────────────────────────────────────

    def _markdown_to_pdf(self, content: str, path: Path) -> Path:
        """Converts markdown-formatted content to a PDF file using fpdf2."""
        try:
            from fpdf import FPDF, XPos, YPos

            pdf = FPDF()
            pdf.add_page()
            pdf.set_left_margin(20)
            pdf.set_right_margin(20)
            pdf.set_top_margin(20)
            pdf.set_auto_page_break(auto=True, margin=20)

            # Try Arial TrueType for full PT-BR Unicode support
            font_name = "Helvetica"
            unicode_ok = False

            if platform.system() == "Windows":
                arial = Path(r"C:\Windows\Fonts\arial.ttf")
                arialbd = Path(r"C:\Windows\Fonts\arialbd.ttf")
                if arial.exists() and arialbd.exists():
                    try:
                        pdf.add_font("F", "", str(arial))
                        pdf.add_font("F", "B", str(arialbd))
                        font_name = "F"
                        unicode_ok = True
                    except Exception:
                        pass

            def _t(txt: str) -> str:
                """Encode text for the active font."""
                if unicode_ok:
                    return txt
                return txt.encode("latin-1", errors="replace").decode("latin-1")

            def _write(txt: str, style: str = "", size: int = 10, lh: int = 6):
                pdf.set_font(font_name, style, size)
                pdf.multi_cell(0, lh, _t(txt), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            for line in content.split("\n"):
                raw = line.rstrip()

                if not raw or raw.startswith("<!--"):
                    pdf.ln(2)
                    continue

                if raw == "---":
                    pdf.ln(2)
                    pdf.set_draw_color(180, 180, 180)
                    y = pdf.get_y()
                    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
                    pdf.ln(3)
                    continue

                stripped = raw.lstrip()
                indent = len(raw) - len(stripped)

                if raw.startswith("# ") and not raw.startswith("## "):
                    pdf.ln(2)
                    _write(raw[2:], "B", 15, 8)
                    pdf.ln(2)
                elif raw.startswith("## "):
                    pdf.ln(3)
                    _write(raw[3:], "B", 13, 7)
                    pdf.ln(1)
                elif raw.startswith("### "):
                    pdf.ln(1)
                    _write(raw[4:], "B", 11, 6)
                elif raw.startswith("#### "):
                    _write(raw[5:], "B", 10, 6)
                elif stripped.startswith(("- ", "* ", "• ")):
                    text = re.sub(r"\*\*(.*?)\*\*", r"\1", stripped[2:])
                    indent_str = "  " * (indent // 2)
                    bullet_txt = indent_str + "  •  " + text
                    pdf.set_font(font_name, "", 10)
                    pdf.multi_cell(0, 5, _t(bullet_txt), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                else:
                    text = re.sub(r"\*\*(.*?)\*\*", r"\1", raw)
                    text = re.sub(r"__(.*?)__", r"\1", text)
                    _write(text, "", 10, 5)

            path.parent.mkdir(parents=True, exist_ok=True)
            pdf.output(str(path))
            logger.info(f"PDF salvo: {path}")
            return path

        except Exception as e:
            logger.error(f"Erro ao gerar PDF {path.name}: {e}. Salvando como .txt")
            txt_path = path.with_suffix(".txt")
            txt_path.parent.mkdir(parents=True, exist_ok=True)
            txt_path.write_text(content, encoding="utf-8")
            return txt_path

    # ─── text ─────────────────────────────────────────────────────────────────

    def save_full_package(self, outputs: dict, date_str: str = None) -> dict[str, Path]:
        """
        Saves all text outputs as PDF files, organized by platform.

        Keys accepted:
          instagram_legenda, instagram_carrossel_textos, instagram_engagement,
          tiktok_legenda, tiktok_engagement, tiktok_video_ideia,
          youtube_legenda, youtube_engagement,
          facebook_legenda, facebook_storytelling, facebook_engagement,
          video_master, visual_concept
        """
        date_str = date_str or datetime.now().strftime("%Y-%m-%d")
        saved: dict[str, Path] = {}

        mapping = {
            # ── Instagram ─────────────────────────────────────────────────────
            "instagram_legenda":          ("instagram", "legendas.md"),
            "instagram_carrossel_textos": ("instagram", "carrossel_textos.md"),
            "instagram_engagement":       ("instagram", "engagement_dicas.md"),
            # ── TikTok ───────────────────────────────────────────────────────
            "tiktok_legenda":             ("tiktok",    "legenda_video.md"),
            "tiktok_engagement":          ("tiktok",    "engagement_dicas.md"),
            "tiktok_video_ideia":         ("tiktok",    "video_ideia.md"),
            # ── YouTube ──────────────────────────────────────────────────────
            "youtube_legenda":            ("youtube",   "titulo_descricao.md"),
            "youtube_engagement":         ("youtube",   "engagement_dicas.md"),
            # ── Facebook ─────────────────────────────────────────────────────
            "facebook_legenda":           ("facebook",  "legenda_video.md"),
            "facebook_storytelling":      ("facebook",  "storytelling.md"),
            "facebook_engagement":        ("facebook",  "engagement_dicas.md"),
            # ── Video production package ──────────────────────────────────────
            "video_master":               ("video-criativo", "producao_roteiro.md"),
            # ── Visual concept ────────────────────────────────────────────────
            "visual_concept":             ("visual-conceito", "conceito.md"),
        }

        for key, (plat, filename) in mapping.items():
            content = outputs.get(key, "")
            if content and len(content.strip()) > 50:
                run_dir = self._get_run_dir(date_str)
                path = run_dir / plat / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                saved[key] = path
            elif key in outputs and outputs[key]:
                logger.warning(f"[{key}] ignorado — conteúdo muito curto ({len(outputs.get(key,''))} chars)")

        return saved

    def save_ugc_narration(self, narration_script: str, date_str: str = None) -> Path:
        """Saves the narration/audio script for UGC video editing as PDF."""
        run_dir = self._get_run_dir(date_str)
        path = run_dir / "videos" / "ugc" / "narracao-edicao.pdf"
        content = (
            "# Narração UGC — para edição de vídeo\n\n"
            "_Adicione este áudio em off e estas legendas durante a montagem dos clipes._\n\n"
            + narration_script
        )
        return self._markdown_to_pdf(content, path)

    # ─── index ────────────────────────────────────────────────────────────────

    def generate_index_content(self, run_id: str, outputs: dict, image_outputs: dict, final_review: str) -> str:
        date_str = run_id.split("_")[0]
        lines = [f"# Output da Agência Finlancer — {date_str}\n"]
        
        lines.append("\n## Revisão Final do Brand Director\n")
        lines.append(final_review)

        if "instagram" in outputs:
            lines.append("\n## Instagram\n")
            if outputs["instagram"].get("legendas"):
                lines.append(f"- [Legendas Instagram](/instagram/legendas.md)")
            if outputs["instagram"].get("roteiros"):
                lines.append(f"- [Roteiros Instagram](/instagram/roteiros.md)")
            for img_name in outputs["instagram"].get("images", {}).keys():
                lines.append(f"- [{img_name.replace('_', ' ').title()}](/instagram/images/{img_name}.png)")

        if "facebook" in outputs and outputs["facebook"].get("post"):
            lines.append("\n## Facebook\n")
            lines.append(f"- [Post Storytelling Facebook](/facebook/post_storytelling.md)")

        if "tiktok" in outputs and outputs["tiktok"].get("roteiro_ugc"):
            lines.append("\n## TikTok\n")
            lines.append(f"- [Roteiro UGC TikTok](/tiktok/roteiro_ugc.md)")

        return "\n".join(lines)

    def generate_index(self, date_str: str = None) -> str:
        run_dir = self._get_run_dir(date_str)
        lines = [f"# Output da Agência Finlancer — {date_str or datetime.now().strftime('%Y-%m-%d')}\n"]
        for plat in PLATFORMS:
            platform_dir = run_dir / plat
            files = (
                list(platform_dir.glob("*.pdf"))
                + list(platform_dir.glob("*.txt"))
                + list(platform_dir.glob("*.png"))
                + list(platform_dir.glob("*.mp4"))
            )
            for sub in platform_dir.iterdir():
                if sub.is_dir():
                    files += list(sub.glob("*.mp4")) + list(sub.glob("*.png")) + list(sub.glob("*.pdf"))
            if files:
                lines.append(f"\n## {plat.title()}")
                for f in sorted(set(files)):
                    lines.append(f"- [{f.name}]({f.relative_to(run_dir)})")

        # This generate_index is for local file system, not for Drive. Main.py will handle Drive index.
        index_content = self.generate_index_content(date_str, {}, {}, "") # Placeholder, actual content from main.py
        index_path = run_dir / "INDEX.md"
        index_path.write_text(index_content, encoding="utf-8")
        return str(index_path)

    def _sanitize(self, text: str) -> str:
        return re.sub(r"[^\w\-_.]", "_", text)[:50]
