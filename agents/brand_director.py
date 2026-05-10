import base64
import logging
from pathlib import Path
from typing import Optional, List, Dict

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class BrandDirector(BaseAgent):
    agent_key = "brand_director"

    def create_daily_briefing(self, date_str: str, trending_topic: str = "", seasonal_note: str = "") -> str:
        prompt = f"""Crie o briefing diário para {date_str}.

Trending topic identificado: {trending_topic or "Pesquise e defina com base no nicho MEI/freelancer/finanças"}
Nota sazonal: {seasonal_note or "Verifique o calendário fiscal — DAS, IRPF, datas relevantes"}

Gere um briefing completo com:
1. Tema do dia e pilar de conteúdo
2. Demandas para cada agente (Copy Specialist, Visual Creator, Video Script)
3. Diferencial Finlancer a destacar
4. CTA sugerido
5. Restrições específicas se houver

Use o template do Brand Director."""
        return self.run(prompt, reset_history=True)

    def review_content(self, content_package: dict, model: str = None) -> str:
        formatted = "\n\n".join(
            f"### {agent.upper()}\n{output}" for agent, output in content_package.items()
        )
        prompt = f"""Revise o pacote de conteúdo abaixo e forneça:

1. STATUS geral (APROVADO / REVISAR / BLOQUEADO)
2. Avaliação de cada peça individualmente
3. Feedback específico para ajustes necessários
4. Lista de conteúdos aprovados para publicação

PACOTE DE CONTEÚDO:
{formatted}

Verifique: tom de voz, CTA presente, segunda pessoa, ausência de proibidos, menção ao diferencial PF+PJ."""
        return self.run(prompt)

    def select_reference_image(self, reference_dir: Path) -> Optional[Path]:
        """
        Reviews all images in reference_dir using Gemini vision.
        """
        candidates = sorted(
            list(reference_dir.glob("*.png"))
            + list(reference_dir.glob("*.jpg"))
            + list(reference_dir.glob("*.jpeg")),
            key=lambda p: p.name,
        )
        if not candidates:
            return None

        # For now, we'll just return the first one or implement a simple selection
        # Gemini vision integration in BaseAgent.run would be needed for full port
        return candidates[0]

    def visual_audit(self, image_paths: list, context: str = "") -> str:
        """
        Reviews generated images.
        """
        return "Auditoria visual: funcionalidade em migração para Gemini Vision."

    def create_weekly_schedule(self, week_start: str = "", seasonal_note: str = "") -> str:
        prompt = f"""Crie o CRONOGRAMA FINAL DE PUBLICAÇÃO para a semana de {week_start}.
Nota sazonal: {seasonal_note}

Organize por:
- Plataforma (Instagram, TikTok, Facebook, YouTube)
- Dia e horário ideal de publicação
- Sequência estratégica
- Justificativa de cada horário escolhido
"""
        return self.run(prompt)

    def create_monthly_plan(self, seasonal_context: str = "", trends_analysis: str = "") -> str:
        prompt = f"""Crie o PLANEJAMENTO MENSAL estratégico.
Contexto sazonal: {seasonal_context}
Análise de tendências: {trends_analysis}

Defina:
1. Objetivos do mês
2. Temas centrais por semana
3. Metas de crescimento
4. Campanhas especiais
"""
        return self.run(prompt)
