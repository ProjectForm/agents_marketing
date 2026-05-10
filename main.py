#!/usr/bin/env python3
"""
Finlancer Marketing Agency — Orquestrador Principal

Uso:
  python main.py                         # Rotina diária completa
  python main.py --weekly                # Planejamento semanal
  python main.py --monthly               # Análise e planejamento mensal
  python main.py --custom "tema aqui"    # Conteúdo sob demanda
  python main.py --date 2025-05-20       # Rotina para data específica
  python main.py --no-review             # Pular fases 3 e 4 de revisão (mais barato)
"""

import argparse
import logging
import os
import sys
from typing import Optional

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from agents import (
    BrandDirector,
    ContentStrategist,
    SocialCopySpecialist,
    VisualContentCreator,
    VideoScriptSpecialist,
)
from tools import OutputManager, TrendAnalyzer, CalendarGenerator

load_dotenv()

_LOGS_DIR = Path(__file__).parent / "logs"
_LOGS_DIR.mkdir(exist_ok=True)
(Path(__file__).parent / "output").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(_LOGS_DIR / f"agency-{datetime.now().strftime('%Y-%m-%d')}.log",
                            encoding="utf-8"),
    ],
)
logger = logging.getLogger("finlancer-agency")

_HAIKU = "claude-haiku-4-5-20251001"
_REVIEW_MAX_CHARS = 2500


def _trim(text: str, max_chars: int = _REVIEW_MAX_CHARS) -> str:
    """Truncate text for review inputs to reduce token cost."""
    if not text or len(text) <= max_chars:
        return text or ""
    return text[:max_chars] + "\n...[truncado]"


def _init_anthropic() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY não encontrada. Configure no arquivo .env")
        sys.exit(1)
    return Anthropic(api_key=api_key)


# ─────────────────────────────────────────────────────────────────────────────
# DAILY ROUTINE
# ─────────────────────────────────────────────────────────────────────────────

def run_daily_routine(
    date_str: str = None,
    custom_theme: str = None,
    run_review: bool = True,
) -> dict:
    """Executes the full daily content production routine."""
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    run_id = date_str + "_" + datetime.now().strftime("%H%M%S")
    logger.info(f"=== ROTINA DIÁRIA — {run_id} ===")

    client = _init_anthropic()
    trend_analyzer = TrendAnalyzer()
    output_manager = OutputManager()
    run_dir = Path(__file__).parent / "output" / run_id

    # Instantiate agents
    brand_director = BrandDirector(client)
    content_strategist = ContentStrategist(client)
    copy_specialist = SocialCopySpecialist(client)
    visual_creator = VisualContentCreator(client)
    video_specialist = VideoScriptSpecialist(client)

    # ─── PHASE 1: Planning Meeting ────────────────────────────────────────────
    logger.info("FASE 1: Planning Meeting")
    seasonal_context = trend_analyzer.get_weekly_brief_context()

    briefing = brand_director.create_daily_briefing(
        date_str=date_str,
        trending_topic=custom_theme,
        seasonal_note=seasonal_context,
    )
    if custom_theme:
        logger.info(f"Tema customizado: {custom_theme}")

    logger.info("Briefing do dia gerado")
    print("\n" + "=" * 60)
    print("BRIEFING DO DIA")
    print("=" * 60)
    print(briefing)

    calendar = CalendarGenerator()
    days_to_das = calendar.days_until_das()
    seasonal_note = seasonal_context
    if days_to_das <= 7:
        seasonal_note += f"\n\nURGENTE: DAS vence em {days_to_das} dia(s)!"

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
        carousel = visual_creator.create_carousel_concept(
            theme=theme_for_day, num_slides=8, briefing=briefing,
        )
        feed = visual_creator.create_feed_concept(
            theme=theme_for_day, briefing=briefing,
        )
        return f"## CARROSSEL\n\n{carousel}\n\n---\n\n## FEED\n\n{feed}"

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
        logger.info("FASE 3: Revisao do Content Strategist (Haiku)")
        return content_strategist.run(
            f"""Revise o pacote de conteúdo abaixo (tema: {theme_for_day[:200]}):

COPY:
{_trim(production_results.get('copy', 'N/A'))}

VISUAL:
{_trim(production_results.get('visual', 'N/A'))}

VIDEO:
{_trim(production_results.get('video', 'N/A'))}

Verifique coerência, tom e alinhamento com o briefing. Seja breve.""",
            model=_HAIKU,
        )

    specialist_review = _review_phase()

    # ─── PHASE 4: Final Approval — Brand Director ──────────────────────────────
    logger.info("FASE 4: Aprovacao Final — Brand Director")

    if run_review:
        logger.info("FASE 4: Revisao textual final (Haiku)")
        final_review = brand_director.review_content(
            {
                "copy_specialist": _trim(production_results.get("copy", "")),
                "visual_creator": _trim(production_results.get("visual", "")),
                "video_specialist": _trim(production_results.get("video", "")),
                "specialist_review": _trim(specialist_review, max_chars=1000),
            },
            model=_HAIKU,
        )
    else:
        final_review = "STATUS: APROVADO\n(revisão automática pulada via --no-review)"
    logger.info("Brand Director concluiu revisao")

    # ─── PHASE 5: Save everything ─────────────────────────────────────────────
    logger.info("FASE 5: Salvando outputs")

    copy_output = production_results.get("copy", "")
    video_output = production_results.get("video", "")
    visual_output = production_results.get("visual", "")

    text_outputs = {
        # ── Instagram ──────────────────────────────────────────────────────
        "instagram_legenda":          _extract_section(copy_output, "INSTAGRAM_LEGENDA"),
        "instagram_carrossel_textos": _extract_section(copy_output, "INSTAGRAM_CARROSSEL_TEXTOS"),
        "instagram_engagement":       _extract_section(copy_output, "INSTAGRAM_ENGAGEMENT"),
        # ── TikTok ─────────────────────────────────────────────────────────
        "tiktok_legenda":             _extract_section(copy_output, "TIKTOK_LEGENDA"),
        "tiktok_engagement":          _extract_section(copy_output, "TIKTOK_ENGAGEMENT"),
        "tiktok_video_ideia":         _extract_section(copy_output, "TIKTOK_VIDEO_IDEIA"),
        # ── YouTube ────────────────────────────────────────────────────────
        "youtube_legenda":            _extract_section(copy_output, "YOUTUBE_LEGENDA"),
        "youtube_engagement":         _extract_section(copy_output, "YOUTUBE_ENGAGEMENT"),
        # ── Facebook ───────────────────────────────────────────────────────
        "facebook_legenda":           _extract_section(copy_output, "FACEBOOK_LEGENDA"),
        "facebook_storytelling":      _extract_section(copy_output, "FACEBOOK_STORYTELLING"),
        "facebook_engagement":        _extract_section(copy_output, "FACEBOOK_ENGAGEMENT"),
        # ── Video production package ────────────────────────────────────────
        "video_master":               video_output,
        # ── Visual concept ─────────────────────────────────────────────────
        "visual_concept":             visual_output,
    }

    approval_header = f"<!-- Aprovado pelo Brand Director em {date_str} -->\n\n"
    text_outputs = {k: approval_header + v for k, v in text_outputs.items() if v}

    saved_files = output_manager.save_full_package(text_outputs, run_id)

    # Save Brand Director review
    if final_review:
        review_path = run_dir / "REVISAO-FINAL.pdf"
        run_dir.mkdir(parents=True, exist_ok=True)
        output_manager._markdown_to_pdf(
            f"# Revisão Final — {run_id}\n\n{final_review}", review_path
        )
        logger.info(f"Revisao final salva: {review_path}")

    index_path = output_manager.generate_index(run_id)
    _print_summary(run_id, saved_files, final_review)

    return {
        "date": date_str,
        "run_id": run_id,
        "briefing": briefing,
        "outputs": production_results,
        "final_review": final_review,
        "saved_files": {k: str(v) for k, v in saved_files.items()},
        "index": index_path,
    }


# ─────────────────────────────────────────────────────────────────────────────
# WEEKLY PLANNING
# ─────────────────────────────────────────────────────────────────────────────

def run_weekly_planning(week_start: str = None) -> dict:
    week_start = week_start or datetime.now().strftime("%Y-%m-%d")
    logger.info(f"=== PLANEJAMENTO SEMANAL — semana de {week_start} ===")

    client = _init_anthropic()
    trend_analyzer = TrendAnalyzer()
    calendar_gen = CalendarGenerator()

    brand_director = BrandDirector(client)
    content_strategist = ContentStrategist(client)
    visual_creator = VisualContentCreator(client)

    trend_context = trend_analyzer.get_weekly_brief_context(
        datetime.strptime(week_start, "%Y-%m-%d")
    )
    logger.info("Contexto de tendencias obtido")

    weekly_calendar = content_strategist.create_weekly_calendar(
        week_start=week_start,
        trending_topics=trend_analyzer.get_content_suggestions(3),
    )
    logger.info("Calendario editorial gerado")

    weekly_palette = visual_creator.create_weekly_palette(
        week_theme="Organizacao Financeira MEI",
        seasonal_context=trend_context,
    )
    logger.info("Paleta semanal gerada")

    validation = brand_director.run(
        f"""Valide o planejamento semanal a seguir e gere o CRONOGRAMA FINAL DE PUBLICAÇÃO
com os melhores horários para máximo engajamento.

CALENDÁRIO EDITORIAL:
{weekly_calendar}

PALETA VISUAL:
{weekly_palette}

CONTEXTO SAZONAL:
{trend_context}

Entregue:
1. Aprovação ou ajustes do calendário
2. Cronograma de publicação completo (dia, hora, plataforma, tipo de post)
3. Sequência estratégica de posts para máximo engajamento
4. Meta de alcance semanal estimada"""
    )

    week_dates = calendar_gen.get_week_dates(datetime.strptime(week_start, "%Y-%m-%d"))
    calendar_template = calendar_gen.generate_weekly_template(week_dates)
    calendar_path = calendar_gen.save_weekly_calendar(weekly_calendar + "\n\n---\n\n" + validation)

    logger.info(f"Planejamento semanal concluido. Calendario: {calendar_path}")
    print("\n" + "=" * 60)
    print("CRONOGRAMA SEMANAL — VISAO DE MAXIMO ENGAJAMENTO")
    print("=" * 60)
    print(validation)

    return {
        "week_start": week_start,
        "calendar": weekly_calendar,
        "palette": weekly_palette,
        "schedule": validation,
        "calendar_path": str(calendar_path),
    }


# ─────────────────────────────────────────────────────────────────────────────
# MONTHLY PLANNING
# ─────────────────────────────────────────────────────────────────────────────

def run_monthly_planning() -> dict:
    month_str = datetime.now().strftime("%B %Y")
    logger.info(f"=== PLANEJAMENTO MENSAL — {month_str} ===")

    client = _init_anthropic()
    trend_analyzer = TrendAnalyzer()
    brand_director = BrandDirector(client)
    content_strategist = ContentStrategist(client)

    seasonal = trend_analyzer.get_seasonal_context()
    trends_analysis = content_strategist.analyze_trends()

    monthly_plan = brand_director.run(
        f"""Crie o planejamento de conteúdo mensal para {month_str}.

ANÁLISE DE TENDÊNCIAS:
{trends_analysis}

CONTEXTO SAZONAL DO MÊS:
Eventos: {', '.join(seasonal['month_events'])}
Tópicos urgentes: {', '.join(seasonal['urgent_topics'])}

Entregue o PLANO MENSAL COMPLETO com:
1. Campanhas especiais do mês (se houver)
2. Distribuição de pilares por semana
3. Meta de output mensal
4. Oportunidades de conteúdo único do mês
5. Estratégia de crescimento para o período
6. Datas fiscais para cobertura de conteúdo"""
    )

    output_path = Path(__file__).parent / "output" / "calendarios"
    output_path.mkdir(parents=True, exist_ok=True)
    plan_file = output_path / f"planejamento-{datetime.now().strftime('%Y-%m')}.pdf"

    from tools import OutputManager
    OutputManager()._markdown_to_pdf(
        f"# Planejamento Mensal — {month_str}\n\n" + monthly_plan, plan_file
    )

    logger.info(f"Planejamento mensal salvo: {plan_file}")
    return {"month": month_str, "plan": monthly_plan, "path": str(plan_file)}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _extract_section(text: str, section_name: str) -> str:
    """
    Extracts content under a section header. Supports both:
    - ## SECTION_NAME (markdown heading)
    - ## SECTION NAME (with spaces instead of underscores)
    Stops at the next ## heading of the same or lower depth.
    """
    if not text:
        return ""

    import re as _re
    needle = section_name.upper().replace("_", "[ _]?")
    lines = text.split("\n")
    in_section = False
    result_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") and _re.search(needle, line.upper()):
            in_section = True
            result_lines.append(line)
            continue
        if in_section:
            if stripped.startswith("##") and not _re.search(needle, line.upper()):
                break
            result_lines.append(line)

    return "\n".join(result_lines).strip()


def _print_summary(run_id: str, saved_files: dict, final_review: str) -> None:
    print("\n" + "=" * 60)
    print(f"RESUMO — Producao de {run_id}")
    print("=" * 60)

    print(f"\nArquivos gerados ({len(saved_files)}):")
    for key, path in saved_files.items():
        print(f"  OK {key}: {Path(path).name}")

    print("\nSTATUS FINAL (Brand Director):")
    review_lines = final_review.split("\n")[:15]
    print("\n".join(review_lines))
    print("\n" + "=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Finlancer Marketing Agency — Orquestrador de Conteudo com IA"
    )
    parser.add_argument("--weekly", action="store_true", help="Executar planejamento semanal")
    parser.add_argument("--monthly", action="store_true", help="Executar planejamento mensal")
    parser.add_argument("--custom", type=str, help="Tema customizado para producao sob demanda")
    parser.add_argument("--date", type=str, help="Data especifica (YYYY-MM-DD)")
    parser.add_argument(
        "--no-review", action="store_true",
        help="Pular fases 3 e 4 de revisao (mais barato, economiza ~40%% do custo)"
    )
    args = parser.parse_args()

    do_review = not args.no_review

    if args.weekly:
        run_weekly_planning(week_start=args.date)
    elif args.monthly:
        run_monthly_planning()
    elif args.custom or args.date:
        run_daily_routine(date_str=args.date, custom_theme=args.custom, run_review=do_review)
    else:
        run_daily_routine(date_str=args.date, run_review=do_review)


if __name__ == "__main__":
    main()
