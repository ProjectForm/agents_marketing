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
from agents.social_copy_specialist import SocialCopySpecialist
from agents.visual_content_creator import VisualContentCreator
from agents.video_script_specialist import VideoScriptSpecialist
from agents.image_generator import ImageGeneratorAgent
from agents.video_generator import VideoGeneratorAgent
from utils.output_parser import OutputParser
from utils.drive_manager import DriveManager
from utils.visual_renderer import VisualRenderer
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
    # Pattern more robust to single or double newlines
    pattern = rf"## {section_name}\s*\n+(.*?)(?=\n## |$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def run_daily_routine(date_str=None, custom_theme=None, use_review=True, no_images=False, no_drive=False, no_video=False, only_phases=None, skip_phases=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    only_phases_set = set(map(int, only_phases.split(','))) if only_phases else None
    skip_phases_set = set(map(int, skip_phases.split(','))) if skip_phases else None

    def _should_run_phase(phase_id):
        if only_phases_set is not None and phase_id not in only_phases_set:
            return False
        if skip_phases_set is not None and phase_id in skip_phases_set:
            return False
        return True
    
    run_id = f"{date_str}_{datetime.now().strftime('%H%M%S')}"
    logger.info(f"=== ROTINA DIÁRIA — {run_id} ===")

    # Initialize Tools
    output_manager = OutputManager()
    output_parser = OutputParser()
    image_generator = ImageGeneratorAgent()
    visual_renderer = VisualRenderer()
    video_generator = VideoGeneratorAgent()
    drive_manager = DriveManager()

    # ─── PHASE 1: Planning ────────────────────────────────────────────────────
    if _should_run_phase(1):
        logger.info("FASE 1: Planning Meeting")
    planner = BaseAgent("content_strategist")
    theme_for_day = custom_theme or "Organização financeira para freelancers CLT + MEI"
    plan = planner.run(f"Planeje o conteúdo para o dia {date_str}. Tema: {theme_for_day}")

    # ─── PHASE 2: Production ──────────────────────────────────────────────────
    if _should_run_phase(2):
        logger.info("FASE 2: Producao de Conteudo (paralela)")
    
    copy_agent = SocialCopySpecialist()
    visual_agent = VisualContentCreator()
    video_script_agent = VideoScriptSpecialist()

    logger.info("Copy Specialist produzindo...")
    copy_output = copy_agent.create_full_copy_package(theme_for_day, plan)
    logger.info("copy concluido")

    logger.info("Visual Creator produzindo conceito...")
    # We need both feed and carousel concepts
    visual_output = {
        "feed": visual_agent.create_feed_concept(theme_for_day, plan),
        "carousel": visual_agent.create_carousel_concept(theme_for_day, 8, plan),
        "ugc_brief": visual_agent.create_ugc_visual_brief("MEI Freelancer", theme_for_day)
    }
    visual_output_raw = json.dumps(visual_output, indent=2, ensure_ascii=False)
    logger.info("visual concluido")

    logger.info("Video Script Specialist produzindo roteiros...")
    video_output = video_script_agent.create_daily_video_package(theme_for_day, plan)
    logger.info("video concluido")

    production_results = {
        "copy": copy_output,
        "visual": visual_output,
        "video": video_output
    }

    # ─── PHASE 3: Review ──────────────────────────────────────────────────────
    if _should_run_phase(3) and use_review:
        logger.info("FASE 3: Revisao do Content Strategist (Gemini)")
        review_feedback = planner.run(f"Revise o conteúdo produzido: {json.dumps(production_results, ensure_ascii=False)}")
    
    # ─── PHASE 4: Final Approval ──────────────────────────────────────────────
    if _should_run_phase(4):
        logger.info("FASE 4: Aprovacao Final — Brand Director")
    brand_director = BaseAgent("brand_director")
    final_review = brand_director.run(f"Dê o veredito final e ajustes finos: {json.dumps(production_results, ensure_ascii=False)}")
    logger.info("Brand Director concluiu revisao")

    # ─── PHASE 5: Image Generation ────────────────────────────────────────────
    image_outputs = {}
    if _should_run_phase(5) and not no_images:
        logger.info("FASE 5: Geracao de Imagens")
        try:


            feed_image_data = visual_output.get("feed_image", {})
            if feed_image_data.get("overlay_text") and feed_image_data.get("background_prompt"):
                image_outputs["feed_image_path"] = visual_renderer.create_feed_image(
                    title=feed_image_data["overlay_text"],
                    illustration_prompt=feed_image_data["background_prompt"],
                    style="Light Mode Finlancer",
                    output_path=output_manager.base_dir / run_id / "01_feed" / "feed_estatico.png"
                )
                time.sleep(7)

            carousel_data = visual_output.get("carousel", {})
            carousel_slides = carousel_data.get("slides", [])
            carousel_images_paths = []
            for i, slide_data in enumerate(carousel_slides):
                if slide_data.get("title") or slide_data.get("body"):
                    pexels_query = slide_data.get("background_prompt", "fintech light mode")
                    background_image_url = visual_renderer.search_pexels_image(pexels_query, orientation="portrait")

                    if background_image_url:
                        img_path = visual_renderer.create_carousel_slide(
                            slide_data=slide_data,
                            background_image_url=background_image_url,
                            output_path=output_manager.base_dir / run_id / "02_carrossel" / f"carrossel_slide_{i+1:02d}.png"
                        )
                        carousel_images_paths.append(img_path)
                    else:
                        logger.warning(f"Nao foi possivel encontrar imagem para o slide {i+1}. Gerando placeholder.")
                        img_path = visual_renderer.create_carousel_slide(
                            slide_data=slide_data,
                            background_image_url="https://via.placeholder.com/1080x1350.png?text=Placeholder",
                            output_path=output_manager.base_dir / run_id / "02_carrossel" / f"carrossel_slide_{i+1:02d}.png"
                        )
                        carousel_images_paths.append(img_path)
                    time.sleep(7)
            image_outputs["carousel_images_paths"] = carousel_images_paths

            ugc_persona_image_data = visual_output.get("ugc_persona_image", {})
            ugc_persona_desc = ugc_persona_image_data.get("prompt", "A Brazilian professional freelancer, authentic and relatable.")
            if ugc_persona_desc:
                image_outputs["ugc_persona_thumbnail_path"] = image_generator.generate_ugc_persona_image(
                    persona_desc=ugc_persona_desc,
                    output_dir=str(output_manager.base_dir / run_id / "03_ugc_video")
                )
                time.sleep(7)
        except Exception as e:
            logger.error(f"Erro na geracao de imagens: {e}")

    # ─── PHASE 6: Video Generation ────────────────────────────────────────────
    video_files = []
    if _should_run_phase(6) and not no_video:
        logger.info("FASE 6: Geracao de Video UGC (4 clipes)")
        try:

            roteiro_ugc = _extract_section(video_output, "ROTEIRO CENA A CENA")
            ugc_persona_desc_for_video = visual_output.get("ugc_persona_image", {}).get("prompt", "A Brazilian professional freelancer, authentic and relatable.")
            # Regex para extrair cada bloco de cena
            cena_blocks = re.findall(r"(\[\d{2}:\d{2}-\d{2}:\d{2}\]\s*.*?)(?=\n\[\d{2}:\d{2}-\d{2}:\d{2}\]|$)", roteiro_ugc, re.DOTALL)
            
            if not cena_blocks:
                logger.warning("Nao foi possivel extrair blocos de cena do roteiro. Usando placeholders.")
                cena_blocks = ["[00:00-00:07] Clipe 1. FALA: 'Olá!' AÇÃO NA TELA: Sorri. EMOÇÃO: Feliz. DESCRIÇÃO VISUAL: Home office.",
                               "[00:07-00:14] Clipe 2. FALA: 'Problema.' AÇÃO NA TELA: Expressão de dúvida. EMOÇÃO: Confuso. DESCRIÇÃO VISUAL: Mesa bagunçada.",
                               "[00:14-00:21] Clipe 3. FALA: 'Solução!' AÇÃO NA TELA: Aponta para o celular. EMOÇÃO: Aliviado. DESCRIÇÃO VISUAL: Usando o app Finlancer.",
                               "[00:21-00:28] Clipe 4. FALA: 'Experimente!' AÇÃO NA TELA: Convida com a mão. EMOÇÃO: Confiante. DESCRIÇÃO VISUAL: Fundo claro, logo Finlancer."]

            # Garantir que temos exatamente 4 clipes
            pontos = cena_blocks[:4]
            while len(pontos) < 4:
                pontos.append("[00:00-00:07] Clipe Extra. FALA: 'Mais dicas!' AÇÃO NA TELA: Sorri. EMOÇÃO: Neutro. DESCRIÇÃO VISUAL: Fundo neutro.")
            
            video_files = video_generator.generate_ugc_video(
                roteiro_pontos=pontos,
                persona_desc=ugc_persona_desc,
                output_dir=str(output_manager.base_dir / run_id / "03_ugc_video")
            )
        except Exception as e:
            logger.error(f"Erro na geracao de video: {e}")

    # ─── PHASE 7: Save everything locally ─────────────────────────────────────
    if _should_run_phase(7):
        logger.info("FASE 7: Salvando outputs localmente")

    text_outputs = {
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
        "visual_concept":             visual_output_raw,
        "video_master":               _extract_section(video_output, "VIDEO_MASTER"),
        "briefing_producao":          _extract_section(video_output, "BRIEFING_PRODUCAO"),
        "cenas_detalhadas":           _extract_section(video_output, "CENAS_DETALHADAS"),
        "narracao_completa":          _extract_section(video_output, "NARRACAO_COMPLETA"),
        "overlay_plataforma":         _extract_section(video_output, "TEXTO_OVERLAY_POR_PLATAFORMA"),
        "trilha_sonora":              _extract_section(video_output, "TRILHA_SONORA"),
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
    if _should_run_phase(8) and not no_drive:
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
    parser.add_argument("--only", type=str, help="Executar apenas fases específicas (ex: 1,3,5)")
    parser.add_argument("--skip", type=str, help="Pular fases específicas (ex: 2,4)")
    
    args = parser.parse_args()
    
    try:
        run_daily_routine(args.date, args.custom, not args.no_review, args.no_images, args.no_drive, args.no_video, args.only, args.skip)
        logger.info(f"Rotina concluída com sucesso para {args.date or datetime.now().strftime('%Y-%m-%d')}")
    except Exception as e:
        logger.error(f"Falha crítica na rotina: {e}", exc_info=True)

if __name__ == "__main__":
    main()
