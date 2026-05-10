import json
import logging
import re
from pathlib import Path
from typing import Optional, Dict, Any

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

def _clean_json_response(text: str) -> str:
    """Remove markdown code blocks and other noise from JSON response."""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    return text.strip()

class VisualContentCreator(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        super().__init__("visual_content_creator", model_name)

    def create_carousel_concept(self, theme: str, num_slides: int, briefing: str) -> Dict[str, Any]:
        prompt = f"""Crie o conceito visual completo para um carrossel de {num_slides} slides.

Tema: {theme}
Briefing: {briefing}

Entregue:
1. WIREFRAME SLIDE-A-SLIDE com:
   - Layout e composição de cada slide
   - Posicionamento de elementos (título, texto, ícone, fundo)
   - Cores específicas (hex codes)
   - Tipografia (família, peso, tamanho em px)
   - Elemento decorativo/gráfico sugerido
   - **visual_hint**: Uma descrição concisa (máximo 50 palavras) do que a imagem de fundo de cada slide deve conter, focando em elementos abstratos e cores, sem texto legível.

2. PALETA DA PEÇA (mantendo identidade Finlancer: emerald #10b981, dark mode)

3. INSTRUÇÕES DE EXECUÇÃO NO CANVA (passo a passo para reproduzir)

Formato: 1080x1350px (4:5). Use dark mode obrigatoriamente.

Responda em formato JSON com as chaves 'concept', 'palette', 'canva_instructions' e 'visual_hints' (lista de strings, uma para cada slide)."""
        raw_output = self.run(prompt, reset_history=True)
        clean_output = _clean_json_response(raw_output)
        try:
            parsed_output = json.loads(clean_output)
            return parsed_output
        except json.JSONDecodeError:
            logger.error(f"Falha ao parsear JSON do carrossel: {raw_output}")
            return {"concept": raw_output, "palette": "", "canva_instructions": "", "visual_hints": []}

    def create_feed_concept(self, theme: str, briefing: str) -> Dict[str, Any]:
        prompt = f"""Crie o conceito visual para 1 post de feed estático.

Tema: {theme}
Briefing: {briefing}

Entregue:
1. Conceito visual completo (layout, composição, hierarquia)
2. Texto de título e subtítulo (máx. 8 e 12 palavras)
3. Paleta de cores com hex codes
4. Instrução de execução no Canva
5. **visual_hint**: Uma descrição concisa (máximo 50 palavras) do que a imagem de fundo deve conter, focando em elementos abstratos e cores, sem texto legível.

Formato: 1080x1080px (1:1) ou 1080x1350px (4:5). Dark mode obrigatório.

Responda em formato JSON com as chaves 'concept', 'title', 'subtitle', 'palette', 'canva_instructions' e 'visual_hint' (string)."""
        raw_output = self.run(prompt)
        clean_output = _clean_json_response(raw_output)
        try:
            parsed_output = json.loads(clean_output)
            return parsed_output
        except json.JSONDecodeError:
            logger.error(f"Falha ao parsear JSON do feed: {raw_output}")
            return {"concept": raw_output, "title": "", "subtitle": "", "palette": "", "canva_instructions": "", "visual_hint": ""}

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

    def extract_visual_hints(self, text_output: str, num_slides: int = 0) -> list[str]:
        """Extrai visual_hints de um output textual, seja para carrossel ou feed."""
        clean_text = _clean_json_response(text_output)
        try:
            data = json.loads(clean_text)
            if num_slides > 0:
                return data.get('visual_hints', [])[:num_slides]
            else:
                hint = data.get('visual_hint', '')
                return [hint] if hint else []
        except json.JSONDecodeError:
            # Fallback regex if JSON is still broken
            if num_slides > 0: # Carrossel
                match = re.search(r'"visual_hints":\s*\[([^\]]+)\]', clean_text)
                if match:
                    try:
                        hints_str = f"[{match.group(1)}]"
                        hints = json.loads(hints_str)
                        return [h for h in hints if isinstance(h, str)][:num_slides]
                    except json.JSONDecodeError:
                        pass
                return ["" for _ in range(num_slides)]
            else: # Feed
                match = re.search(r'"visual_hint":\s*"([^"]+)"', clean_text)
                if match:
                    return [match.group(1)]
                return [""]
