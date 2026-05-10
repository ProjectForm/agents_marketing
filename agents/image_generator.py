import os
import logging
from pathlib import Path
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

FINLANCER_VISUAL_IDENTITY = """
Dark mode fintech design. Background color #0f172a (deep navy/dark slate).
Primary accent color emerald green #10b981. 
Glassmorphism UI cards with subtle blur effect and rgba(255,255,255,0.1) borders.
Border radius 12-20px on all elements.
Typography: Inter or Poppins font family, clean and minimal.
Color palette: background #0f172a, surface #1e293b, primary #10b981, 
gradient from #10b981 to #0ea5e9, text #f1f5f9, secondary text #94a3b8.
High contrast, professional, trustworthy Brazilian fintech aesthetic.
Never white background. Always dark mode.
"""

# Nano Banana 2 (Gemini 3.1 Flash Image)
IMAGEN_MODEL = "imagen-3.1-flash-generate-001"

class ImageGeneratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.output_base_dir = Path(__file__).parent.parent / "output"

    def _generate_image(self, prompt: str, width: int, height: int, output_path: Path) -> str:
        try:
            response = self.client.models.generate_images(
                model=IMAGEN_MODEL,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1" if width == height else ("4:5" if height > width and height/width < 1.5 else "9:16"),
                    output_mime_type="image/png",
                )
            )
            
            if not response.generated_images:
                logger.error(f"Nenhuma imagem gerada para o prompt: {prompt[:50]}...")
                return ""

            image_bytes = response.generated_images[0].image.image_bytes
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            logger.info(f"Imagem gerada e salva em: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Erro ao gerar imagem para prompt '{prompt[:50]}...': {e}")
            return ""

    def generate_carousel_slides(self, visual_hints: list[str], theme: str, date_str: str) -> dict:
        output_dir = self.output_base_dir / date_str / "instagram" / "images"
        generated_images = {}
        for i, hint in enumerate(visual_hints):
            slide_name = f"carrossel_slide_{i+1:02d}"
            prompt = f"{FINLANCER_VISUAL_IDENTITY}\n\nTema do dia: {theme}\n\n{hint}\n\nFormato: 1080x1350px. Imagem de fundo para slide de carrossel. Sem texto legível na imagem."
            output_path = output_dir / f"{slide_name}.png"
            generated_images[slide_name] = self._generate_image(prompt, 1080, 1350, output_path)
        return generated_images

    def generate_feed_image(self, visual_hint: str, theme: str, date_str: str) -> dict:
        output_dir = self.output_base_dir / date_str / "instagram" / "images"
        slide_name = "feed_estatico"
        prompt = f"{FINLANCER_VISUAL_IDENTITY}\n\nTema do dia: {theme}\n\n{visual_hint}\n\nFormato: 1080x1080px. Imagem para post de feed estático. Sem texto legível na imagem."
        output_path = output_dir / f"{slide_name}.png"
        return {slide_name: self._generate_image(prompt, 1080, 1080, output_path)}

    def generate_reel_cover(self, visual_hint: str, theme: str, date_str: str) -> dict:
        output_dir = self.output_base_dir / date_str / "instagram" / "images"
        slide_name = "reel_cover"
        prompt = f"{FINLANCER_VISUAL_IDENTITY}\n\nTema do dia: {theme}\n\n{visual_hint}\n\nFormato: 1080x1920px. Capa para Reel. Texto APENAS no terço superior. Sem texto legível na imagem, apenas elementos visuais que sugiram espaço para texto no terço superior."
        output_path = output_dir / f"{slide_name}.png"
        return {slide_name: self._generate_image(prompt, 1080, 1920, output_path)}
