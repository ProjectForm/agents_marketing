import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Imagen 4 Fast — melhor custo-benefício (sua conta tem Imagen 4, não Imagen 2)
IMAGEN_MODEL = "imagen-4.0-fast-generate-001"


class ImageGenerator:
    """
    Generates actual image files using Google Imagen 2 via the google-genai SDK.

    Aspect ratios supported by Imagen 2: "1:1", "4:3", "3:4", "16:9", "9:16"
    """

    def __init__(self):
        from tools.google_ai_client import get_google_client
        self.client = get_google_client()

    # ─── core ────────────────────────────────────────────────────────────────

    def _generate(self, prompt: str, aspect_ratio: str = "1:1", count: int = 1) -> list[bytes]:
        from google.genai import types

        response = self.client.models.generate_images(
            model=IMAGEN_MODEL,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=count,
                aspect_ratio=aspect_ratio,
                safety_filter_level="block_low_and_above",
                person_generation="allow_adult",
            ),
        )
        return [img.image.image_bytes for img in response.generated_images]

    def _save(self, image_bytes: bytes, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(image_bytes)
        logger.info(f"Imagem salva: {path}")
        return path

    # ─── public ──────────────────────────────────────────────────────────────

    def generate_ugc_persona(self, theme: str, output_dir: Path) -> Optional[Path]:
        """
        Generates a consistent base image of a Brazilian person for UGC videos.
        This image is used as the character reference across all 5 Veo clips.
        Returns the saved PNG path, or None on failure.
        """
        prompt = (
            "Photorealistic portrait of a Brazilian professional, 28-34 years old, "
            "gender-neutral friendly appearance, looking directly at camera with a warm confident smile. "
            "Setting: modern bright home office, large window with natural daylight, "
            "blurred bookshelf and plants in background. "
            "Wearing smart-casual clothes — plain light shirt, no logos. "
            "Hands slightly visible, relaxed posture. Smartphone on desk nearby. "
            "Cinematic shallow depth of field, 4K quality. "
            "NO text, NO watermarks, NO logos anywhere in the image."
        )
        try:
            images = self._generate(prompt, aspect_ratio="9:16")
            if not images:
                logger.warning("Imagen 2 não retornou imagens para persona UGC.")
                return None
            return self._save(images[0], output_dir / "ugc-persona-base.png")
        except Exception as e:
            logger.error(f"Erro ao gerar persona UGC: {e}")
            return None

    def generate_carousel_slides(
        self,
        prompts: list[str],
        output_dir: Path,
    ) -> list[Optional[Path]]:
        """
        Generates one image per prompt for carousel slides (4:5, 1080x1350px equivalent).
        Returns list of paths (None for any slide that failed).
        """
        paths: list[Optional[Path]] = []
        for i, prompt in enumerate(prompts, start=1):
            try:
                images = self._generate(prompt, aspect_ratio="4:3")
                if images:
                    path = self._save(images[0], output_dir / f"slide-{i:02d}.png")
                    paths.append(path)
                else:
                    logger.warning(f"Imagen 2 sem resultado para slide {i}.")
                    paths.append(None)
            except Exception as e:
                logger.error(f"Erro ao gerar slide {i}: {e}")
                paths.append(None)
        return paths

    def generate_feed_image(
        self,
        prompt: str,
        output_dir: Path,
        filename: str = "feed-post.png",
    ) -> Optional[Path]:
        """Generates a single 1:1 feed post image. Returns saved path or None."""
        try:
            images = self._generate(prompt, aspect_ratio="1:1")
            if not images:
                return None
            return self._save(images[0], output_dir / filename)
        except Exception as e:
            logger.error(f"Erro ao gerar imagem de feed: {e}")
            return None
