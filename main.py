import argparse
import json
import logging
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from agents import (
    BrandDirector,
    ContentStrategist,
    SocialCopySpecialist,
    VisualContentCreator,
    VideoScriptSpecialist,
    ImageGeneratorAgent,
)
from tools import OutputManager, DriveManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(f"logs/agency-{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("finlancer-agency")

_GEMINI_MODEL = "gemini-2.5-flash"
_REVIEW_MAX_CHARS = 5000

def _extract_section(text: str, section_name: str) -> str:
    pattern = re.compile(rf"## {section_name}\n\n(.*?)(?=\n## |$)", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return ""

def _trim(text: str, max_chars: int = _REVIEW_MAX_CHARS) -> str:
    """Truncate text for review inputs to reduce token cost."""
    if not text or len(text) <= max_chars:
        return text or ""
    return text[:max_chars] + "\n...[truncado]"


def _print_summary(run_id: str, saved_local_files: dict[str, Path], final_review: str, uploaded_drive_links: dict = None):
    logger.info("\n" + "=" * 60)
    logger.info(f"RESUMO DA EXECUÇÃO {run_id}")
    logger.info("=" * 60)
    logger.info(f"Revisão Final do Brand Director: {final_review[:100]}...")
    logger.info("-" * 60)
    logger.info("Arquivos Locais Salvos:")
    for key, path in saved_local_files.items():
        logger.info(f"  - {key}: {path}")
    
    if uploaded_drive_links and uploaded_drive_links.get("day_folder_link"):
        logger.info("-" * 60)
        logger.info(f"Google Drive: {uploaded_drive_links['day_folder_link']}")
    logger.info("=" * 60 + "\n")


def run_daily_routine(
    date_str: str = None,
    custom_theme: str = None,
    run_review: bool = True,
    no_images: bool = False,
    no_drive: bool = False,
) -> dict:
    """Executes the full daily content production routine."""
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    run_id = date_str + "_" + datetime.now().strftime("%H%M%S")
    logger.info(f"=== ROTINA DIÁRIA — {run_id} ===")

    output_manager = OutputManager()
    drive_manager = None
    if not no_drive:
        try:
            drive_manager = DriveManager()
        except Exception as e:
            logger.error(f"Falha ao inicializar DriveManager: {e}. Upload para Drive sera desativado.")
            no_drive = True

    # Instantiate agents
    brand_director = BrandDirector()
    content_strategist = ContentStrategist()
    copy_specialist = SocialCopySpecialist()
    visual_creator = VisualContentCreator()
    video_specialist = VideoScriptSpecialist()
    image_generator = ImageGeneratorAgent()

    # ─── PHASE 1: Planning Meeting ────────────────────────────────────────────
    logger.info("FASE 1: Planning Meeting")
    # In a real scenario, we would use TrendAnalyzer here.
    # For this evolution, we'll use the custom theme or a default briefing.
    briefing = """Foco na persona 'Carla' (32 anos, consultora de marketing, CLT + MEI). 
    Ela sofre com a confusão entre finanças pessoais e do negócio, especialmente agora em maio com o IRPF e o DASN-SIMEI.
    Diferencial Finlancer: Visão unificada PF+PJ e IA Consultiva (Fin) para tirar dúvidas fiscais."""
    
    theme_for_day = custom_theme or briefing

    # ─── PHASE 2: Parallel Text Production ────────────────────────────────────
    logger.info("FASE 2: Producao de Conteudo (paralela)")
    production_results: dict = {}

    def run_copy():
        logger.info("Copy Specialist produzindo...")
        return copy_specialist.create_full_copy_package(
            theme=theme_for_day,
            briefing=briefing,
        )

    def run_visual():
        logger.info("Visual Creator produzindo conceito...")
        carousel_concept = visual_creator.create_carousel_concept(
            theme=theme_for_day, num_slides=8, briefing=briefing,
        )
        feed_concept = visual_creator.create_feed_concept(
            theme=theme_for_day, briefing=briefing,
        )
        return {"carousel": carousel_concept, "feed": feed_concept}

    def run_video_scripts():
        logger.info("Video Script Specialist produzindo roteiros...")
        return video_specialist.create_daily_video_package(
            theme=theme_for_day, briefing=briefing,
        )

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(run_copy): "copy",
            executor.submit(run_visual): "visual",
            executor.submit(run_video_scripts): "video",
        }
        for future in as_completed(futures):
            key = futures[future]
            try:
                production_results[key] = future.result()
                logger.info(f"{key} concluido")
            except Exception as e:
                logger.error(f"Erro em {key}: {e}")
                production_results[key] = f"[ERRO: {e}]"

    # ─── PHASE 3: Content Strategist Review ───────────────────────────────────
    def _review_phase():
        if not run_review:
            logger.info("FASE 3: Revisao pulada (--no-review)")
            return "(revisão pulada via --no-review)"
        logger.info("FASE 3: Revisao do Content Strategist (Gemini)")
        visual_review_text = ""
        if isinstance(production_results.get("visual"), dict):
            carousel_concept = production_results["visual"].get("carousel", {})
            feed_concept = production_results["visual"].get("feed", {})
            visual_review_text += f"## CARROSSEL\n\n{carousel_concept.get('concept', 'N/A')}\n\n"
            visual_review_text += f"## FEED\n\n{feed_concept.get('concept', 'N/A')}"
        else:
            visual_review_text = production_results.get("visual", "N/A")

        return content_strategist.run(
            f"""Revise o pacote de conteúdo abaixo (tema: {theme_for_day[:200]}):

COPY:
{_trim(production_results.get("copy", "N/A"))}

VISUAL:
{_trim(visual_review_text)}

VIDEO:
{_trim(production_results.get("video", "N/A"))}

Verifique coerência, tom e alinhamento com o briefing. Seja breve."""
        )

    specialist_review = _review_phase()

    # ─── PHASE 4: Final Approval — Brand Director ──────────────────────────────
    logger.info("FASE 4: Aprovacao Final — Brand Director")

    if run_review:
        logger.info("FASE 4: Revisao textual final (Gemini)")
        visual_review_text = ""
        if isinstance(production_results.get("visual"), dict):
            carousel_concept = production_results["visual"].get("carousel", {})
            feed_concept = production_results["visual"].get("feed", {})
            visual_review_text += f"## CARROSSEL\n\n{carousel_concept.get('concept', 'N/A')}\n\n"
            visual_review_text += f"## FEED\n\n{feed_concept.get('concept', 'N/A')}"
        else:
            visual_review_text = production_results.get("visual", "N/A")

        final_review = brand_director.review_content(
            {
                "copy_specialist": _trim(production_results.get("copy", "")),
                "visual_creator": _trim(visual_review_text),
                "video_specialist": _trim(production_results.get("video", "")),
                "specialist_review": _trim(specialist_review, max_chars=1000),
            }
        )
    else:
        final_review = "STATUS: APROVADO\n(revisão automática pulada via --no-review)"
    logger.info("Brand Director concluiu revisao")

    # ─── PHASE 5: Image Generation ────────────────────────────────────────────
    image_outputs = {}
    if not no_images:
        logger.info("FASE 5: Geracao de Imagens")
        try:
            visual_concepts = production_results.get("visual", {})
            carousel_concept = visual_concepts.get("carousel", {})
            feed_concept = visual_concepts.get("feed", {})

            carousel_visual_hints = carousel_concept.get("visual_hints", [])
            feed_visual_hint = feed_concept.get("visual_hint", "")

            if carousel_visual_hints:
                image_outputs.update(image_generator.generate_carousel_slides(carousel_visual_hints, theme_for_day, date_str))
            if feed_visual_hint:
                image_outputs.update(image_generator.generate_feed_image(feed_visual_hint, theme_for_day, date_str))
            
            reel_cover_hint = feed_concept.get("visual_hint", "")
            if reel_cover_hint:
                image_outputs.update(image_generator.generate_reel_cover(reel_cover_hint, theme_for_day, date_str))

        except Exception as e:
            logger.error(f"Erro na geracao de imagens: {e}")

    # ─── PHASE 6: Upload to Google Drive ──────────────────────────────────────
    uploaded_drive_links = {}
    if not no_drive:
        logger.info("FASE 6: Upload para Google Drive")
        copy_output = production_results.get("copy", "")
        video_output = production_results.get("video", "")

        outputs_for_drive = {
            "instagram": {
                "legendas": _extract_section(copy_output, "INSTAGRAM_LEGENDA"),
                "roteiros": _extract_section(copy_output, "INSTAGRAM_CARROSSEL_TEXTOS"),
                "images": image_outputs
            },
            "facebook": {
                "post": _extract_section(copy_output, "FACEBOOK_STORYTELLING")
            },
            "tiktok": {
                "roteiro_ugc": _extract_section(video_output, "VIDEO_MASTER")
            },
            "index": "" 
        }
        
        index_content = output_manager.generate_index_content(run_id, outputs_for_drive, image_outputs, final_review)
        outputs_for_drive["index"] = index_content

        uploaded_drive_links = drive_manager.upload_daily_package(date_str, outputs_for_drive)
        logger.info(f"Upload para Google Drive concluido. Pasta do dia: {uploaded_drive_links.get('day_folder_link', 'N/A')}")

    # ─── PHASE 7: Save everything locally ─────────────────────────────────────
    logger.info("FASE 7: Salvando outputs localmente")

    copy_output = production_results.get("copy", "")
    video_output = production_results.get("video", "")
    visual_output_raw = production_results.get("visual", "")

    text_outputs_for_local_save = {
        "instagram_legenda":          _extract_section(copy_output, "INSTAGRAM_LEGENDA"),
        "instagram_carrossel_textos": _extract_section(copy_output, "INSTAGRAM_CARROSSEL_TEXTOS"),
        "instagram_engagement":       _extract_section(copy_output, "INSTAGRAM_ENGAGEMENT"),
        "tiktok_legenda":             _extract_section(copy_output, "TIKTOK_LEGENDA"),
        "tiktok_engagement":          _extract_section(copy_output, "TIKTOK_ENGAGEMENT"),
        "tiktok_video_ideia":         _extract_section(copy_output, "TIKTOK_VIDEO_IDEIA"),
        "youtube_legenda":            _extract_section(copy_output, "YOUTUBE_LEGENDA"),
        "youtube_engagement":         _extract_section(copy_output, "YOUTUBE_ENGAGEMENT"),
        "facebook_legenda":           _extract_section(copy_output, "FACEBOOK_LEGENDA"),
        "facebook_storytelling":      _extract_section(copy_output, "FACEBOOK_STORYTELLING"),
        "facebook_engagement":        _extract_section(copy_output, "FACEBOOK_ENGAGEMENT"),
        "video_master":               video_output,
        "visual_concept":             visual_output_raw,
    }

    approval_header = f"<!-- Aprovado pelo Brand Director em {date_str} -->\n\n"
    
    def _ensure_str(v):
        if isinstance(v, dict):
            return json.dumps(v, indent=2, ensure_ascii=False)
        return str(v)

    text_outputs_for_local_save = {k: approval_header + _ensure_str(v) for k, v in text_outputs_for_local_save.items() if v}

    saved_local_files = output_manager.save_full_package(text_outputs_for_local_save, run_id)

    if final_review:
        run_dir = output_manager.base_dir / run_id
        review_path = run_dir / "REVISAO-FINAL.md"
        run_dir.mkdir(parents=True, exist_ok=True)
        review_path.write_text(f"# Revisão Final — {run_id}\n\n{final_review}", encoding="utf-8")
        logger.info(f"Revisao final salva: {review_path}")

    index_path = output_manager.generate_index(run_id)
    _print_summary(run_id, saved_local_files, final_review, uploaded_drive_links)

    return {
        "date": date_str,
        "run_id": run_id,
        "briefing": briefing,
        "outputs": production_results,
        "final_review": final_review,
        "saved_local_files": {k: str(v) for k, v in saved_local_files.items()},
        "image_outputs": image_outputs,
        "uploaded_drive_links": uploaded_drive_links,
    }


def main():
    parser = argparse.ArgumentParser(description="Agência Finlancer — Produção de Conteúdo")
    parser.add_argument("--date", type=str, help="Data para produção (YYYY-MM-DD)")
    parser.add_argument("--custom", type=str, help="Tema customizado para o dia")
    parser.add_argument("--no-review", action="store_true", help="Pular fase de revisão")
    parser.add_argument("--no-images", action="store_true", help="Pular geração de imagens")
    parser.add_argument("--no-drive", action="store_true", help="Pular upload para Google Drive")
    
    args = parser.parse_args()

    try:
        result = run_daily_routine(args.date, args.custom, not args.no_review, args.no_images, args.no_drive)
        logger.info(f"Rotina concluída com sucesso para {result['date']}")
    except Exception as e:
        logger.error(f"Falha crítica na rotina: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
