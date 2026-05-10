import base64
import logging
from pathlib import Path
from typing import Optional

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
        return self.run(prompt, model=model)

    def select_reference_image(self, reference_dir: Path) -> Optional[Path]:
        """
        Reviews all images in reference_dir using Claude vision.
        Returns the best one for Veo 3 generation: person mid-speech, clear face,
        vertical/portrait framing, no hands/screens in focus.
        Returns None if no suitable image found.
        """
        candidates = sorted(
            list(reference_dir.glob("*.png"))
            + list(reference_dir.glob("*.jpg"))
            + list(reference_dir.glob("*.jpeg")),
            key=lambda p: p.name,
        )
        if not candidates:
            logger.info("Pasta de referências vazia.")
            return None

        content: list = [{
            "type": "text",
            "text": (
                "Selecione a MELHOR imagem de referência para geração de vídeo UGC no Veo 3.\n\n"
                "CRITÉRIOS (em ordem de prioridade):\n"
                "1. Pessoa claramente no ato da fala — boca levemente aberta, expressão de conversa\n"
                "2. Rosto nítido e bem iluminado, sem sombras pesadas\n"
                "3. Formato vertical (9:16) ou retrato — ideal para Reels/TikTok\n"
                "4. Mãos fora do foco ou fora do quadro (mãos causam distorção no Veo)\n"
                "5. Fundo simples ou desfocado — menos elementos = melhor para o Veo\n"
                "6. Sem tela de celular ou monitor em destaque\n\n"
                "DESCARTE SE: sem rosto visível, de costas, objeto é o elemento principal.\n\n"
                "Responda em 1 linha:\n"
                "SELECIONADA: [número] — [motivo objetivo]\n"
                "Se nenhuma qualificar: NENHUMA — [motivo]"
            ),
        }]

        for i, path in enumerate(candidates, 1):
            try:
                img_b64 = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
                media_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
                content.append({"type": "text", "text": f"[Imagem {i}: {path.name}]"})
                content.append({
                    "type": "image",
                    "source": {"type": "base64", "media_type": media_type, "data": img_b64},
                })
            except Exception as e:
                logger.warning(f"Não foi possível carregar {path.name}: {e}")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=150,
            messages=[{"role": "user", "content": content}],
        )
        result = response.content[0].text.strip()
        logger.info(f"Seleção de referência: {result}")

        import re as _re
        match = _re.search(r"SELECIONADA:\s*(\d+)", result, _re.IGNORECASE)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(candidates):
                selected = candidates[idx]
                logger.info(f"Imagem de referência selecionada: {selected.name}")
                return selected

        logger.warning("Nenhuma imagem de referência qualificada.")
        return None

    def visual_audit(self, image_paths: list, context: str = "") -> str:
        """
        Reviews up to 3 generated PNG images using Claude vision.
        Checks for AI artifacts: hand distortion, garbled text, brand palette, generic look.
        Returns structured audit report.
        """
        content = []
        loaded = 0

        for raw_path in image_paths[:3]:  # max 3 images to control cost
            p = Path(raw_path) if raw_path else None
            if not p or not p.exists():
                continue
            try:
                img_b64 = base64.standard_b64encode(p.read_bytes()).decode("utf-8")
                content.append({"type": "text", "text": f"[Imagem: {p.name}]"})
                content.append({
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": img_b64},
                })
                loaded += 1
            except Exception as e:
                logger.warning(f"Não foi possível carregar {p} para auditoria visual: {e}")

        if loaded == 0:
            return "Auditoria visual: nenhuma imagem disponível."

        audit_prompt = {
            "type": "text",
            "text": f"""Brand Director auditando {loaded} imagem(ns) gerada(s) pelo Imagen 4.
Contexto: {context or 'Imagens para publicação nas redes sociais do Finlancer'}

Para cada imagem, execute e informe cada item:

ARTEFATOS DE IA (mais comuns no Imagen):
□ Mãos/dedos: normais ou distorcidos/extras?
□ Texto na imagem: ausente (ok) ou com artefatos/garbled?
□ Proporções gerais: anatomia natural ou deformada?

IDENTIDADE VISUAL FINLANCER:
□ Fundo dark mode (#0f172a ou escuro equivalente)?
□ Emerald (#10b981) presente como cor de destaque?
□ Parece app financeiro brasileiro ou stock photo genérico?

AUTENTICIDADE:
□ A imagem tem personalidade visual ou parece banco de imagens internacional?
□ Poderia ser publicada como está ou precisa de retrabalho?

VEREDICTO por imagem:
✓ APROVADA — [nome]: [motivo objetivo]
✗ REPROVADA — [nome]: [problema exato] → [como corrigir o prompt Imagen]""",
        }
        content.insert(0, audit_prompt)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=[{
                "type": "text",
                "text": self.system_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": content}],
        )
        return response.content[0].text

    def create_weekly_schedule(self, week_content: list[dict]) -> str:
        prompt = f"""Com base nos conteúdos aprovados desta semana, crie o CRONOGRAMA FINAL DE PUBLICAÇÃO
com a visão de máximo engajamento possível.

CONTEÚDOS DA SEMANA:
{week_content}

Organize por:
- Plataforma (Instagram, TikTok, Facebook, YouTube)
- Dia e horário ideal de publicação
- Sequência estratégica (ex: carrossel educacional → reel de impacto → post de engajamento)
- Justificativa de cada horário escolhido

Inclua visão consolidada: total de posts por plataforma e cobertura semanal."""
        return self.run(prompt)
