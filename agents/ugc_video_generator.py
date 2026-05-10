"""
UGC Video Generator — Veo 3 (Google)

Workflow:
1. Claude (BaseAgent) crafts 5 short Veo prompts: Hook, Dev1, Dev2, Dev3, CTA
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

from anthropic import Anthropic

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

VEO_MODEL = "veo-3.0-generate-001"       # versão estável (sua conta tem 3.0 e 3.1)
VEO_FALLBACK = "veo-2.0-generate-001"  # fallback se 3.0 falhar
MAX_POLL_SECONDS = 360   # 6 minutes max per video
POLL_INTERVAL = 12       # check every 12 seconds
MAX_CLIP_RETRIES = 2     # retries on quality failure (with simplified prompt)
MIN_CLIP_KB = 150        # minimum file size — smaller = likely corrupt/empty render


def _simplify_veo_prompt(prompt: str, attempt: int) -> str:
    """
    Progressively simplifies a Veo prompt to reduce distortion on retry.
    Attempt 1: remove hands/screen mentions, cap at 2 visual elements.
    Attempt 2: ultra-minimal — expression + camera only, guaranteed safe.
    """
    import re as _re

    if attempt >= 2:
        # Ultra-minimal fallback — works on virtually every Veo call
        return (
            "Person looks directly at camera with a natural, engaged expression, "
            "slight forward lean, soft natural window light, medium close-up, "
            "static camera, warm background slightly out of focus, no hands visible."
        )

    # Attempt 1: strip known distortion triggers
    # Remove clauses mentioning hands, screens, typing, phones
    cleaned = _re.sub(
        r"[^.]*\b(hand|finger|dedo|mão|digita|celular|tela|phone|screen|type|keyboard|tecla)\b[^.]*[.,]?",
        "",
        prompt,
        flags=_re.IGNORECASE,
    ).strip()

    # If more than 3 comma-separated actions, keep only the first 2 + camera
    parts = [p.strip() for p in cleaned.split(",") if p.strip()]
    camera_parts = [p for p in parts if any(w in p.lower() for w in ["zoom", "rack", "steadicam", "camera", "câmera", "shot", "close"])]
    action_parts = [p for p in parts if p not in camera_parts]
    simplified = ", ".join((action_parts[:2] + camera_parts[:1]))

    return simplified or prompt


class UGCVideoGenerator(BaseAgent):
    """
    Generates UGC-style short video sequences using Veo 3.

    Produces 5 clips (Hook + 3 Development + CTA) that form a complete
    vertical-video UGC narrative when assembled in a video editor.
    Narration/audio is separate from the video generation (added in editing).
    """

    agent_key = "ugc_video_generator"

    def __init__(self, anthropic_client: Anthropic):
        super().__init__(anthropic_client)
        self._google_client = None

    # ─── Google client ────────────────────────────────────────────────────────

    def _get_google(self):
        if self._google_client is None:
            from tools.google_ai_client import get_google_client
            self._google_client = get_google_client()
        return self._google_client

    # ─── Prompt crafting (Claude) ─────────────────────────────────────────────

    def _craft_video_prompts(self, theme: str, briefing: str, has_reference: bool) -> list[dict]:
        """Uses Claude to generate 5 Veo-optimized prompts + narration per clip."""
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
   — o Veo 3 não renderiza texto corretamente e o clipe fica bugado
2. Descreva APENAS: ação física, expressão facial, movimento de câmera, iluminação, ambiente
3. Máximo 2 frases curtas por prompt de vídeo
4. Use vocabulário cinematográfico: "close-up", "câmera revela lentamente",
   "luz natural suave", "rack focus", "steadicam"
5. Cada clipe deve ter ação visual clara e distinta dos outros

━━ ESTRUTURA (narração é áudio/legenda em edição — NÃO vai no Veo) ━━
Clipe 1 — GANCHO (≤8s): Reação de impacto, olha para câmera surpreso/intrigado, câmera se aproxima
Clipe 2 — DEV 1 (≤8s): Conta nos dedos, expressão séria explicativa, luz lateral
Clipe 3 — DEV 2 (≤8s): Aponta para fora de campo, expressão de revelação, leve zoom in
Clipe 4 — DEV 3 (≤8s): Segura e olha para smartphone, alívio/solução encontrada, luz de tela
Clipe 5 — CTA (≤7s): Sorri, aponta direto para câmera, gesto de convite confiante, bright key light

━━ FORMATO DE RESPOSTA ━━
Responda APENAS JSON válido, sem texto fora do JSON:
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

narracao_off = o que a pessoa FALA em off (máx 12 palavras, em português)"""

        raw = self.run(prompt, reset_history=True)

        match = re.search(r'\[[\s\S]*\]', raw)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError as e:
                logger.warning(f"Falha ao parsear JSON de prompts de vídeo: {e}")

        logger.warning("Usando prompts de fallback para os vídeos.")
        return _fallback_prompts(theme)

    # ─── Veo 3 operations ─────────────────────────────────────────────────────

    def _submit_video(
        self,
        veo_prompt: str,
        reference_bytes: Optional[bytes],
        duration: int,
        model: str = VEO_MODEL,
    ):
        """Submits a video generation operation to Veo. Returns the operation object."""
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
        """Polls an operation until done, then saves the video. Returns success bool."""
        client = self._get_google()
        elapsed = 0

        while not operation.done and elapsed < MAX_POLL_SECONDS:
            time.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL
            try:
                # SDK v1.74+: get() aceita o nome como keyword arg
                operation = client.operations.get(name=operation.name)
            except TypeError:
                # fallback para SDK mais antiga que aceita o objeto diretamente
                try:
                    operation = client.operations.get(operation)
                except Exception as e:
                    logger.warning(f"Erro ao consultar operação: {e}")
            except Exception as e:
                logger.warning(f"Erro ao consultar operação: {e}")

        if not operation.done:
            logger.error(f"Timeout ({MAX_POLL_SECONDS}s) para {output_path.name}")
            return False

        if operation.error:
            logger.error(f"Veo retornou erro: {operation.error}")
            return False

        generated = getattr(operation.result, "generated_videos", [])
        if not generated:
            logger.error("Nenhum vídeo retornado pelo Veo.")
            return False

        video = generated[0].video
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if getattr(video, "video_bytes", None):
            output_path.write_bytes(video.video_bytes)
        elif getattr(video, "uri", None):
            urllib.request.urlretrieve(video.uri, str(output_path))
        else:
            logger.error("Vídeo sem dados para salvar (sem bytes nem URI).")
            return False

        logger.info(f"Vídeo salvo: {output_path} ({output_path.stat().st_size // 1024} KB)")
        return True

    def _generate_one(self, spec: dict, reference_bytes: Optional[bytes], output_dir: Path) -> dict:
        """
        Generates a single clip with up to MAX_CLIP_RETRIES retries.
        On each retry, the prompt is progressively simplified to reduce distortion.
        Quality gate: file must be >= MIN_CLIP_KB to be considered valid.
        """
        clip_num = spec["clip"]
        tipo = spec["tipo"]
        original_prompt = spec["veo_prompt"]
        duration = spec.get("segundos", 7)
        filename = f"ugc-{clip_num:02d}-{tipo.lower().replace(' ', '-')}.mp4"
        output_path = output_dir / filename

        for attempt in range(MAX_CLIP_RETRIES + 1):
            prompt = original_prompt if attempt == 0 else _simplify_veo_prompt(original_prompt, attempt)
            if attempt > 0:
                logger.info(f"Clipe {clip_num} — retry {attempt} com prompt simplificado")
                logger.debug(f"Prompt simplificado: {prompt}")

            # Submit to Veo 3, fallback to Veo 2 on submit error
            operation = None
            for model in (VEO_MODEL, VEO_FALLBACK):
                try:
                    operation = self._submit_video(prompt, reference_bytes, duration, model=model)
                    break
                except Exception as e:
                    logger.warning(f"Clipe {clip_num} submit com {model} falhou: {e}")

            if operation is None:
                logger.error(f"Clipe {clip_num}: nenhum modelo aceitou o submit.")
                if attempt < MAX_CLIP_RETRIES:
                    continue
                return {**spec, "veo_prompt": prompt, "path": None, "success": False}

            # Wait for completion and save
            logger.info(f"Clipe {clip_num}/5 ({tipo}) submetido — aguardando Veo...")
            success = self._wait_and_save(operation, output_path)

            if not success:
                logger.warning(f"Clipe {clip_num}: _wait_and_save retornou False.")
                if attempt < MAX_CLIP_RETRIES:
                    continue
                return {**spec, "veo_prompt": prompt, "path": None, "success": False}

            # Quality gate: reject suspiciously small files
            file_kb = output_path.stat().st_size // 1024
            if file_kb < MIN_CLIP_KB:
                logger.warning(
                    f"Clipe {clip_num}: arquivo {file_kb}KB < mínimo {MIN_CLIP_KB}KB "
                    f"— possível render vazio ou distorcido."
                )
                if attempt < MAX_CLIP_RETRIES:
                    output_path.unlink(missing_ok=True)
                    continue
                return {**spec, "veo_prompt": prompt, "path": None, "success": False}

            logger.info(f"Clipe {clip_num} OK — {file_kb}KB (tentativa {attempt + 1})")
            return {**spec, "veo_prompt": prompt, "path": str(output_path), "success": True}

        return {**spec, "veo_prompt": original_prompt, "path": None, "success": False}

    # ─── public ──────────────────────────────────────────────────────────────

    def generate_ugc_sequence(
        self,
        theme: str,
        briefing: str,
        reference_image_path: Optional[Path],
        output_dir: Path,
    ) -> dict:
        """
        Full UGC pipeline: craft prompts → submit all 5 to Veo simultaneously
        → wait for all → save clips.

        Returns dict with:
          - clips: list of per-clip results (veo_prompt, narracao_off, path, success)
          - narration_script: formatted narration for video editing
          - output_dir: str path
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        reference_bytes: Optional[bytes] = None
        if reference_image_path and reference_image_path.exists():
            reference_bytes = reference_image_path.read_bytes()
            logger.info(f"Imagem de referência carregada: {reference_image_path.name}")
        else:
            logger.warning("Sem imagem de referência — vídeos sem consistência de personagem.")

        logger.info("Claude gerando prompts Veo 3...")
        specs = self._craft_video_prompts(theme, briefing, has_reference=bool(reference_bytes))

        # Submit all 5 in parallel — each clip takes ~3-5 min but they run concurrently
        results = []
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {
                pool.submit(self._generate_one, spec, reference_bytes, output_dir): spec["clip"]
                for spec in specs
            }
            for future in as_completed(futures):
                clip_num = futures[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f"Clipe {clip_num} falhou inesperadamente: {e}")
                    results.append({"clip": clip_num, "tipo": "?", "path": None, "success": False,
                                    "veo_prompt": "", "narracao_off": ""})

        results.sort(key=lambda r: r["clip"])

        narration_lines = [
            f"{r['clip']}. [{r['tipo']}] {r.get('narracao_off', '')} "
            f"({'OK' if r['success'] else 'FALHOU'})"
            for r in results
        ]

        success_count = sum(1 for r in results if r["success"])
        logger.info(f"UGC concluído: {success_count}/5 clipes gerados.")

        return {
            "clips": results,
            "narration_script": "\n".join(narration_lines),
            "output_dir": str(output_dir),
        }


# ─── Fallback prompts (used if Claude JSON parsing fails) ─────────────────────

def _fallback_prompts(theme: str) -> list[dict]:
    return [
        {
            "clip": 1, "tipo": "GANCHO", "segundos": 7,
            "veo_prompt": (
                "Close-up of person reacting with surprise, eyes wide, slight lean forward toward camera. "
                "Natural window light, soft focus background, camera slowly zooms in."
            ),
            "narracao_off": "Você já cometeu esse erro sendo MEI?",
        },
        {
            "clip": 2, "tipo": "DEV 1", "segundos": 7,
            "veo_prompt": (
                "Person counts on fingers, serious focused expression, gestures to explain a list. "
                "Warm interior key light from left, steadicam holds medium shot."
            ),
            "narracao_off": "São 5 erros que a maioria comete no primeiro ano.",
        },
        {
            "clip": 3, "tipo": "DEV 2", "segundos": 7,
            "veo_prompt": (
                "Person points to something off-screen left, eyebrows raised in revelation. "
                "Camera slowly rack-focuses from background to face, natural daylight."
            ),
            "narracao_off": "O maior deles? Misturar conta pessoal com a do negócio.",
        },
        {
            "clip": 4, "tipo": "DEV 3", "segundos": 7,
            "veo_prompt": (
                "Person holds smartphone, looks at it with relief and soft smile. "
                "Warm screen glow illuminates face, shallow depth of field, camera holds steady."
            ),
            "narracao_off": "O Finlancer separa tudo automaticamente pra você.",
        },
        {
            "clip": 5, "tipo": "CTA", "segundos": 6,
            "veo_prompt": (
                "Person smiles warmly directly at camera, points index finger toward lens in a friendly inviting gesture. "
                "Bright natural key light, confident posture, camera holds on medium close-up."
            ),
            "narracao_off": "Cria sua conta grátis agora. Link na bio.",
        },
    ]
