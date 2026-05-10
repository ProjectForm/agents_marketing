import os
import sys
import time
import logging
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from agents.base_agent import BaseAgent
from agents.image_generator import ImageGeneratorAgent
from agents.video_generator import VideoGeneratorAgent
from utils.output_parser import OutputParser
from utils.drive_manager import DriveManager
from tools.output_manager import OutputManager

# Load environment variables
load_dotenv()

# Configuration
_GEMINI_MODEL = "gemini-2.5-flash"

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(f"logs/agency-{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("finlancer-agency")

def _extract_section(text, section_name):
    """Helper to extract sections from agent output based on headers like ## SECTION_NAME"""
    pattern = rf"## {section_name}\n\n(.*?)(?=\n## |$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def run_daily_routine(date_str=None, custom_theme=None, use_review=True, no_images=False, no_drive=False, no_video=False):
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    run_id = f"{date_str}_{datetime.now().strftime('%H%M%S')}"
    logger.info(f"=== ROTINA DIÁRIA — {run_id} ===")

    # Initialize Tools
    output_manager = OutputManager()
    output_parser = OutputParser()
    image_generator = ImageGeneratorAgent()
    video_generator = VideoGeneratorAgent()
    drive_manager = DriveManager()

    # ─── PHASE 1: Planning ────────────────────────────────────────────────────
    logger.info("FASE 1: Planning Meeting")
    planner = BaseAgent("content_strategist")
    theme_for_day = custom_theme or "Organização financeira para freelancers CLT + MEI"
    plan = planner.run(f"Planeje o conteúdo para o dia {date_str}. Tema: {theme_for_day}")

    # ─── PHASE 2: Production ──────────────────────────────────────────────────
    logger.info("FASE 2: Producao de Conteudo (paralela)")
    
    copy_agent = BaseAgent("social_copy_specialist")
    visual_agent = BaseAgent("visual_content_creator")
    video_script_agent = BaseAgent("video_script_specialist")

    logger.info("Copy Specialist produzindo...")
    copy_output = copy_agent.run(f"Crie as legendas para o tema: {theme_for_day}. Plano: {plan}")
    logger.info("copy concluido")

    logger.info("Visual Creator produzindo conceito...")
    visual_output_raw = visual_agent.run(f"Crie o conceito visual para o tema: {theme_for_day}. Plano: {plan}")
    try:
        clean_visual = re.sub(r"```json\n|\n```", "", visual_output_raw).strip()
        visual_output = json.loads(clean_visual)
    except Exception as e:
        logger.error(f"Falha ao parsear JSON do carrossel: {e}")
        visual_output = {"carousel": {"concept": visual_output_raw}}
    logger.info("visual concluido")

    logger.info("Video Script Specialist produzindo roteiros...")
    video_output = video_script_agent.run(f"Crie os roteiros de vídeo para o tema: {theme_for_day}. Plano: {plan}")
    logger.info("video concluido")

    production_results = {
        "copy": copy_output,
        "visual": visual_output,
        "video": video_output
    }

    # ─── PHASE 3: Review ──────────────────────────────────────────────────────
    if use_review:
        logger.info("FASE 3: Revisao do Content Strategist (Gemini)")
        review_feedback = planner.run(f"Revise o conteúdo produzido: {json.dumps(production_results, ensure_ascii=False)}")
    
    # ─── PHASE 4: Final Approval ──────────────────────────────────────────────
    logger.info("FASE 4: Aprovacao Final — Brand Director")
    brand_director = BaseAgent("brand_director")
    final_review = brand_director.run(f"Dê o veredito final e ajustes finos: {json.dumps(production_results, ensure_ascii=False)}")
    logger.info("Brand Director concluiu revisao")

    # ─── PHASE 5: Image Generation ────────────────────────────────────────────
    image_outputs = {}
    if not no_images:
        logger.info("FASE 5: Geracao de Imagens")
        try:
            feed_overlay_text = output_parser.extract_feed_overlay_text(copy_output)
            carousel_slides_data = output_parser.extract_carousel_slides(visual_output)
            ugc_persona_desc = output_parser.extract_ugc_persona_description(video_output)

            if feed_overlay_text:
                image_outputs["feed_image_path"] = image_generator.generate_feed_image(
                    theme=theme_for_day, texto_overlay=feed_overlay_text, output_dir=str(output_manager.base_dir / run_id / "01_feed")
                )
                time.sleep(7)

            carousel_images_paths = []
            for i, slide_data in enumerate(carousel_slides_data):
                if slide_data["titulo"] or slide_data["corpo"]:
                    img_path = image_generator.generate_carousel_slide(
                        slide_num=i+1, titulo=slide_data["titulo"], corpo=slide_data["corpo"],
                        output_dir=str(output_manager.base_dir / run_id / "02_carrossel")
                    )
                    carousel_images_paths.append(img_path)
                    time.sleep(7)
            image_outputs["carousel_images_paths"] = carousel_images_paths

            if ugc_persona_desc:
                image_outputs["ugc_persona_thumbnail_path"] = image_generator.generate_ugc_persona_image(
                    persona_desc=ugc_persona_desc, output_dir=str(output_manager.base_dir / run_id / "03_ugc_video")
                )
                time.sleep(7)
        except Exception as e:
            logger.error(f"Erro na geracao de imagens: {e}")

    # ─── PHASE 6: Video Generation ────────────────────────────────────────────
    video_files = []
    if not no_video:
        logger.info("FASE 6: Geracao de Video UGC (4 clipes)")
        try:
            ugc_persona_desc = output_parser.extract_ugc_persona_description(video_output)
            roteiro_ugc = _extract_section(video_output, "UGC_NARRATION")
            pontos = re.findall(r"(?:CLIPE \d+:|CLIP \d+:|\d\.)\s*(.*?)(?=(?:CLIPE \d+:|CLIP \d+:|\d\.)|$)", roteiro_ugc, re.DOTALL)
            if not pontos:
                pontos = [p.strip() for p in roteiro_ugc.split('\n') if p.strip() and len(p) > 20][:4]
            
            if not pontos:
                pontos = ["Clip 1", "Clip 2", "Clip 3", "Clip 4"]
            
            video_files = video_generator.generate_ugc_video(
                roteiro_pontos=pontos,
                persona_desc=ugc_persona_desc,
                output_dir=str(output_manager.base_dir / run_id / "03_ugc_video")
            )
        except Exception as e:
            logger.error(f"Erro na geracao de video: {e}")

    # ─── PHASE 7: Save everything locally ─────────────────────────────────────
    logger.info("FASE 7: Salvando outputs localmente")

    text_outputs = {
        "instagram_legenda":          _extract_section(copy_output, "LEGENDA 1") or _extract_section(copy_output, "INSTAGRAM_LEGENDA"),
        "instagram_carrossel_textos": _extract_section(copy_output, "LEGENDA 2") or _extract_section(copy_output, "CARROSSEL_TEXTOS"),
        "tiktok_legenda":             _extract_section(copy_output, "LEGENDA 3") or _extract_section(copy_output, "TIKTOK_LEGENDA"),
        "tiktok_video_ideia":         _extract_section(copy_output, "TIKTOK_VIDEO_IDEIA"),
        "visual_concept":             visual_output_raw,
        "ugc_legenda":                _extract_section(video_output, "UGC_NARRATION"),
    }

    approval_header = f"<!-- Aprovado pelo Brand Director em {date_str} -->\n\n"
    all_text_outputs = {k: approval_header + (json.dumps(v, indent=2, ensure_ascii=False) if isinstance(v, dict) else str(v)) for k, v in text_outputs.items() if v}

    saved_local_files = output_manager.save_full_package(
        outputs=all_text_outputs,
        run_id=run_id
    )
    
    # Save final review
    review_path = output_manager.base_dir / run_id / "REVISAO-FINAL.md"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(final_review, encoding="utf-8")
    logger.info(f"Revisao final salva: {review_path}")

    # ─── PHASE 8: Upload to Drive ─────────────────────────────────────────────
    uploaded_drive_links = {}
    if not no_drive:
        logger.info("FASE 8: Upload para Google Drive")
        uploaded_drive_links = drive_manager.create_and_upload_daily_package(
            run_id=run_id,
            text_outputs=text_outputs,
            image_outputs=image_outputs,
            video_files=video_files,
            final_review=final_review,
            output_parser=output_parser
        )
        logger.info(f"Upload para Google Drive concluido. Pasta do dia: {uploaded_drive_links.get('day_folder_link')}")

    _print_summary(run_id, final_review, saved_local_files, uploaded_drive_links.get("day_folder_link"))
    return run_id

def _print_summary(run_id, review, files, drive_link):
    logger.info("\n" + "="*60)
    logger.info(f"RESUMO DA EXECUÇÃO {run_id}")
    logger.info("="*60)
    logger.info(f"Revisão Final do Brand Director: {review[:200]}...")
    logger.info("-" * 60)
    logger.info("Arquivos Locais Salvos:")
    for k, v in files.items():
        logger.info(f"  - {k}: {v}")
    logger.info("-" * 60)
    logger.info(f"Google Drive: {drive_link}")
    logger.info("="*60)

def main():
    parser = argparse.ArgumentParser(description="Finlancer Agency - Daily Content Routine")
    parser.add_argument("--date", type=str, help="Data da rotina (YYYY-MM-DD)")
    parser.add_argument("--custom", type=str, help="Tema customizado para o dia")
    parser.add_argument("--no-review", action="store_true", help="Pular fase de revisao")
    parser.add_argument("--no-images", action="store_true", help="Pular geracao de imagens")
    parser.add_argument("--no-video", action="store_true", help="Pular geracao de video")
    parser.add_argument("--no-drive", action="store_true", help="Pular upload para o Drive")
    
    args = parser.parse_args()
    
    try:
        run_daily_routine(args.date, args.custom, not args.no_review, args.no_images, args.no_drive, args.no_video)
        logger.info(f"Rotina concluída com sucesso para {args.date or datetime.now().strftime('%Y-%m-%d')}")
    except Exception as e:
        logger.error(f"Falha crítica na rotina: {e}", exc_info=True)

if __name__ == "__main__":
    main()
