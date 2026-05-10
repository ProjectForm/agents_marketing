"""
UGC Video Generator — Veo 3 (Google)

Workflow:
1. Gemini (BaseAgent) crafts 5 short Veo prompts: Hook, Dev1, Dev2, Dev3, CTA
2. All 5 video generation operations are submitted to Veo 3 simultaneously
3. Operations are polled in parallel until complete
4. Each clip is max 8 seconds, 9:16, NO text overlays in prompt (causes render bugs)
5. The same reference image is used for all clips to ensure character consistency

Veo 3 constraints known by this agent:
- Max 8 seconds per clip
- Does NOT render text/words reliably — NEVER include text in prompts
- Image-to-video: reference image must be PNG/JPEG, passed as image bytes
- Aspect ratio: 9:16 for vertical (Reels/TikTok)
- Model: veo-3.0-generate-001 (fallback: veo-2.0-generate-001)
- Operations are async — must poll until done
"""

import json
import logging
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

VEO_MODEL = "veo-3.1-lite-generate-preview"       # versão lite recomendada
VEO_FALLBACK = "veo-3.0-generate-001"  # fallback se 3.1 falhar
MAX_POLL_SECONDS = 360   # 6 minutes max per video
POLL_INTERVAL = 12       # check every 12 seconds
MAX_CLIP_RETRIES = 2     # retries on quality failure (with simplified prompt)
MIN_CLIP_KB = 150        # minimum file size — smaller = likely corrupt/empty render


def _simplify_veo_prompt(prompt: str, attempt: int) -> str:
    """
    Progressively simplifies a Veo prompt to reduce distortion on retry.
    """
    import re as _re

    if attempt >= 2:
        return (
            "Person looks directly at camera with a natural, engaged expression, "
            "slight forward lean, soft natural window light, medium close-up, "
            "static camera, warm background slightly out of focus, no hands visible."
        )

    cleaned = _re.sub(
        r"[^.]*\b(hand|finger|dedo|mão|digita|celular|tela|phone|screen|type|keyboard|tecla)\b[^.]*[.,]?",
        "",
        prompt,
        flags=_re.IGNORECASE,
    ).strip()

    parts = [p.strip() for p in cleaned.split(",") if p.strip()]
    camera_parts = [p for p in parts if any(w in p.lower() for w in ["zoom", "rack", "steadicam", "camera", "câmera", "shot", "close"])]
    action_parts = [p for p in parts if p not in camera_parts]
    simplified = ", ".join((action_parts[:2] + camera_parts[:1]))

    return simplified or prompt


class UGCVideoGenerator(BaseAgent):
    """
    Generates UGC-style short video sequences using Veo 3.
    """

    agent_key = "ugc_video_generator"

    def __init__(self, model_name: str = "gemini-2.5-pro"):
        super().__init__(model_name)
        self._google_client = None

    def _get_google(self):
        if self._google_client is None:
            from tools.google_ai_client import get_google_client
            self._google_client = get_google_client()
        return self._google_client

    def _craft_video_prompts(self, theme: str, briefing: str, has_reference: bool) -> list[dict]:
        """Uses Gemini to generate 5 Veo-optimized prompts + narration per clip."""
        ref_note = (
            "A pessoa já está definida na imagem de referência. "
            "NÃO redescreva aparência física — apenas ação, expressão e câmera."
            if has_reference
            else "Descreva uma pessoa brasileira, 28-34 anos, home office iluminado, roupa casual profissional."
        )

        prompt = f"""Você é especialista em geração de vídeo com Veo 3 (Google).

TEMA: {theme}
BRIEFING RESUMIDO: {briefing[:600]}

Crie 5 prompts Veo para uma sequência UGC vertical (9:16). Cada clipe = máximo 8 segundos.
{ref_note}

━━ REGRAS CRÍTICAS DO VEO 3 (VIOLÁ-LAS QUEBRA O VÍDEO) ━━
1. PROIBIDO incluir texto, palavras, letras, legendas ou sobreposições no prompt
2. Descreva APENAS: ação física, expressão facial, movimento de câmera, iluminação, ambiente
3. Máximo 2 frases curtas por prompt de vídeo
4. Use vocabulário cinematográfico: "close-up", "câmera revela lentamente",
   "luz natural suave", "rack focus", "steadicam"
5. Cada clipe deve ter ação visual clara e distinta dos outros

━━ ESTRUTURA ━━
Clipe 1 — GANCHO (≤8s): Reação de impacto, olha para câmera surpreso/intrigado, câmera se aproxima
Clipe 2 — DEV 1 (≤8s): Conta nos dedos, expressão séria explicativa, luz lateral
Clipe 3 — DEV 2 (≤8s): Aponta para fora de campo, expressão de revelação, leve zoom in
Clipe 4 — DEV 3 (≤8s): Segura e olha para smartphone, alívio/solução encontrada, luz de tela
Clipe 5 — CTA (≤7s): Sorri, aponta direto para câmera, gesto de convite confiante, bright key light

━━ FORMATO DE RESPOSTA ━━
Responda APENAS JSON válido:
[
  {{
    "clip": 1,
    "tipo": "GANCHO",
    "veo_prompt": "...",
    "narracao_off": "...",
    "segundos": 7
  }},
  ...5 itens...
]
"""
        raw = self.run(prompt, reset_history=True)
        match = re.search(r'\[[\s\S]*\]', raw)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError as e:
                logger.warning(f"Falha ao parsear JSON de prompts de vídeo: {e}")
        return []

    def _submit_video(self, veo_prompt: str, reference_bytes: Optional[bytes], duration: int, model: str = VEO_MODEL):
        from google.genai import types
        client = self._get_google()
        config = types.GenerateVideosConfig(
            aspect_ratio="9:16",
            duration_seconds=min(duration, 8),
            number_of_videos=1,
        )
        if reference_bytes:
            return client.models.generate_videos(
                model=model,
                prompt=veo_prompt,
                image=types.Image(image_bytes=reference_bytes, mime_type="image/png"),
                config=config,
            )
        return client.models.generate_videos(
            model=model,
            prompt=veo_prompt,
            config=config,
        )

    def _wait_and_save(self, operation, output_path: Path) -> bool:
        client = self._get_google()
        elapsed = 0
        while not operation.done and elapsed < MAX_POLL_SECONDS:
            time.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL
            try:
                operation = client.operations.get(name=operation.name)
            except Exception as e:
                logger.warning(f"Erro ao consultar operação: {e}")
        if not operation.done or operation.error:
            return False
        generated = getattr(operation.result, "generated_videos", [])
        if not generated:
            return False
        video = generated[0].video
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if getattr(video, "video_bytes", None):
            output_path.write_bytes(video.video_bytes)
        elif getattr(video, "uri", None):
            urllib.request.urlretrieve(video.uri, str(output_path))
        else:
            return False
        return True

    def generate_ugc_sequence(self, theme: str, briefing: str, reference_image_path: Optional[str] = None, output_dir: str = "output/videos/ugc") -> list[dict]:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        ref_bytes = None
        if reference_image_path and Path(reference_image_path).exists():
            ref_bytes = Path(reference_image_path).read_bytes()
            
        specs = self._craft_video_prompts(theme, briefing, has_reference=bool(ref_bytes))
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for spec in specs:
                filename = f"ugc-{spec['clip']:02d}-{spec['tipo'].lower()}.mp4"
                path = output_path / filename
                futures.append(executor.submit(self._generate_and_save, spec, ref_bytes, path))
            
            for future in as_completed(futures):
                results.append(future.result())
        
        return results

    def _generate_and_save(self, spec: dict, ref_bytes: Optional[bytes], path: Path) -> dict:
        for attempt in range(MAX_CLIP_RETRIES + 1):
            prompt = spec["veo_prompt"] if attempt == 0 else _simplify_veo_prompt(spec["veo_prompt"], attempt)
            try:
                operation = self._submit_video(prompt, ref_bytes, spec.get("segundos", 7))
                if self._wait_and_save(operation, path):
                    return {**spec, "path": str(path), "success": True}
            except Exception as e:
                logger.error(f"Erro no clipe {spec['clip']}: {e}")
        return {**spec, "path": None, "success": False}
