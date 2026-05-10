import json
import logging
import re
from pathlib import Path
from typing import Optional

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class VisualContentCreator(BaseAgent):
    agent_key = "visual_content_creator"

    # ─── concept text (unchanged — used in review pipeline) ──────────────────

    def create_carousel_concept(self, theme: str, num_slides: int, briefing: str) -> str:
        prompt = f"""Crie o conceito visual completo para um carrossel de {num_slides} slides.

TEMA: {theme}
BRIEFING: {briefing}

Entregue:
1. WIREFRAME SLIDE-A-SLIDE com:
   - Layout e composição de cada slide
   - Posicionamento de elementos (título, texto, ícone, fundo)
   - Cores específicas (hex codes)
   - Tipografia (família, peso, tamanho em px)
   - Elemento decorativo/gráfico sugerido

2. PALETA DA PEÇA (mantendo identidade Finlancer: emerald #10b981, dark mode)

3. INSTRUÇÕES DE EXECUÇÃO NO CANVA (passo a passo para reproduzir)

Formato: 1080x1350px (4:5). Use dark mode obrigatoriamente."""
        return self.run(prompt, reset_history=True)

    def create_feed_concept(self, theme: str, briefing: str) -> str:
        prompt = f"""Crie o conceito visual para 1 post de feed estático.

TEMA: {theme}
BRIEFING: {briefing}

Entregue:
1. Conceito visual completo (layout, composição, hierarquia)
2. Texto de título e subtítulo (máx. 8 e 12 palavras)
3. Paleta de cores com hex codes
4. Instrução de execução no Canva

Formato: 1080x1080px (1:1) ou 1080x1350px (4:5). Dark mode obrigatório."""
        return self.run(prompt)

    def create_ugc_visual_brief(self, persona: str, theme: str) -> str:
        prompt = f"""Crie o briefing visual para gravação de vídeo UGC.

PERSONA: {persona}
TEMA: {theme}

Entregue:
1. Cenário ideal (local, iluminação, fundo)
2. Roupa e aparência sugerida para a persona
3. Configuração de câmera (ângulo, altura, distância)
4. Elementos props recomendados (notebook, celular, etc.)
5. Conceito visual da tela inicial e texto overlay para o reel"""
        return self.run(prompt)

    def create_weekly_palette(self, week_theme: str, seasonal_context: str = "") -> str:
        prompt = f"""Crie a paleta visual da semana para o tema: {week_theme}
Contexto sazonal: {seasonal_context or "padrão — sem campanha especial"}

Entregue:
1. Paleta completa com hex codes e uso de cada cor
2. Diferença e justificativa vs. paleta base Finlancer
3. Variações por formato (feed, carrossel, reels)
4. Elementos visuais recorrentes da semana para consistência de feed"""
        return self.run(prompt, reset_history=True)

    # ─── Imagen 2 prompt generation ───────────────────────────────────────────

    def create_carousel_image_prompts(
        self,
        theme: str,
        briefing: str,
        num_slides: int = 8,
    ) -> list[str]:
        """
        Generates Imagen 2-optimized prompts for each carousel slide (background/base images).
        These are background images — text overlays are added in Canva/editing.
        Returns a list of prompt strings (one per slide).
        """
        prompt = f"""Você gerará prompts para o Imagen 2 (Google) criar imagens de fundo para carrossel.

TEMA: {theme}
NÚMERO DE SLIDES: {num_slides}
BRIEFING: {briefing[:500]}

IDENTIDADE VISUAL FINLANCER:
- Dark mode: fundo #0f172a (quase preto)
- Cor de destaque: emerald #10b981 (verde)
- Estilo: glassmorphism, cards com blur sutil, gradientes escuros
- Tipografia abstrata como elemento visual (não palavras legíveis)

REGRAS PARA OS PROMPTS IMAGEN 2:
1. Descreva apenas elementos visuais ABSTRATOS ou CONCEITUAIS — sem texto legível nas imagens
2. Cada slide deve ter composição diferente mas coerente com a identidade
3. Estilos aceitos: glassmorphism, dark tech, financial data viz, abstract gradients
4. Inclua: cor dominante, estilo, elementos visuais, composição
5. Imagens serão usadas como FUNDO — haverá texto sobreposto em edição
6. Cada prompt: máximo 60 palavras

ESTRUTURA DOS SLIDES:
- Slide 1 (capa): Composição impactante, elemento visual grande, espaço para título
- Slides 2-{num_slides - 1} (conteúdo): Variações de layout, espaço para texto de conteúdo
- Slide {num_slides} (CTA): Gradiente emerald, composição convidativa

Responda APENAS JSON válido:
["prompt do slide 1", "prompt do slide 2", ..., "prompt do slide {num_slides}"]"""

        raw = self.run(prompt, reset_history=True)
        match = re.search(r'\[[\s\S]*\]', raw)
        if match:
            try:
                prompts = json.loads(match.group())
                if isinstance(prompts, list) and all(isinstance(p, str) for p in prompts):
                    return prompts[:num_slides]
            except json.JSONDecodeError:
                pass

        logger.warning("Falha ao parsear prompts de carrossel. Usando fallback.")
        return _fallback_carousel_prompts(theme, num_slides)

    def create_feed_image_prompt(self, theme: str, briefing: str) -> str:
        """Returns a single Imagen 2 prompt for a square feed post background."""
        prompt = f"""Gere 1 prompt para o Imagen 2 criar uma imagem de fundo 1:1 para feed Instagram.

TEMA: {theme}
IDENTIDADE: dark mode, emerald #10b981, glassmorphism, estilo financeiro tech brasileiro

Regras:
- Sem texto legível na imagem (será sobreposto em edição)
- Composição centrada com espaço para overlay
- Máximo 50 palavras

Responda APENAS o prompt, sem explicação."""
        return self.run(prompt, reset_history=True).strip()


# ─── Fallback prompts ─────────────────────────────────────────────────────────

def _fallback_carousel_prompts(theme: str, num_slides: int) -> list[str]:
    base = (
        "Dark mode background #0f172a, emerald green #10b981 accent elements, "
        "glassmorphism card with frosted blur effect, "
        "subtle grid pattern, financial data visualization style, "
        "centered composition with negative space for text overlay, "
        "4K render quality, no text or words visible"
    )
    slides = [
        f"Bold hero composition, large emerald geometric shape, deep dark gradient, {base}",
    ]
    for i in range(2, num_slides):
        slides.append(f"Slide {i} content layout, soft depth lines, minimal {base}")
    slides.append(f"CTA slide, emerald to sky-blue gradient glow, radiant center, {base}")
    return slides[:num_slides]
