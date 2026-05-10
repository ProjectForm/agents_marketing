from google import genai
import os
from pathlib import Path
import time
import logging

logger = logging.getLogger("finlancer-agency")

FINLANCER_STYLE = """
Dark mode fintech design. Solid background #0f172a (deep navy dark slate).
Emerald green #10b981 as primary accent. Glassmorphism UI cards with 
rgba(255,255,255,0.1) border and subtle blur. Inter or Poppins typography, 
bold white text high contrast. Professional Brazilian fintech. 
No white backgrounds. Dark mode only. Minimal, clean, trustworthy.
Gradient elements from #10b981 to #0ea5e9 on highlights.
"""

class ImageGeneratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "imagen-4.0-generate-001"
    
    def generate_image(self, prompt: str, output_path: str, 
                       aspect_ratio: str = "1:1") -> str:
        """
        aspect_ratio: "1:1" para feed, "3:4" para carrossel (fallback de 4:5), "9:16" para reel cover
        Retorna path do arquivo salvo.
        """
        # Imagen 4.0 supports 1:1, 9:16, 16:9, 4:3, 3:4. 4:5 is NOT supported.
        if aspect_ratio == "4:5":
            aspect_ratio = "3:4"
            
        logger.info(f"Gerando imagem com prompt: {prompt[:100]}... (Ratio: {aspect_ratio})")
        try:
            response = self.client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=genai.types.GenerateImagesConfig(
                    output_mime_type="image/png",
                    aspect_ratio=aspect_ratio,
                )
            )
            
            if not response.generated_images:
                logger.error(f"Nenhuma imagem gerada para o prompt: {prompt[:50]}...")
                return ""

            image_data = response.generated_images[0].image.image_bytes
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_data)
            logger.info(f"Imagem salva em: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Erro ao gerar imagem para prompt '{prompt[:50]}...': {e}")
            return f"[ERRO_IMAGEM: {e}]"
    
    def generate_feed_image(self, theme: str, texto_overlay: str, 
                            output_dir: str) -> str:
        """Feed 1080x1080. Retorna path do PNG."""
        prompt = f"""
        {FINLANCER_STYLE}
        Social media feed post 1:1 square format.
        Main topic: {theme}
        Text overlay (bold, top-center): "{texto_overlay}"
        Include: emerald accent card, financial dashboard UI elements,
        subtle chart or graph decoration, @finlancer.app watermark bottom-right.
        Photorealistic fintech app promotional image.
        """
        path = f"{output_dir}/feed_estatico.png"
        return self.generate_image(prompt, path, "1:1")
    
    def generate_carousel_slide(self, slide_num: int, titulo: str, 
                                 corpo: str, output_dir: str) -> str:
        """Slide carrossel 1080x1350. Retorna path do PNG."""
        is_capa = slide_num == 1
        
        if is_capa:
            prompt = f"""
            {FINLANCER_STYLE}
            Instagram carousel cover slide vertical format.
            Bold impact title center: "{titulo}"
            Subtitle below: "{corpo}"
            Large emerald geometric accent shape background.
            Professional, high-impact, invites to swipe right.
            """
        else:
            prompt = f"""
            {FINLANCER_STYLE}
            Instagram carousel content slide {slide_num}, vertical.
            Slide number "{slide_num:02d}" small emerald top-left.
            Title: "{titulo}"
            Body text: "{corpo}"
            Glassmorphism card center, emerald left border accent strip.
            Clean readable layout, minimal elements.
            """
        
        path = f"{output_dir}/carrossel_slide_{slide_num:02d}.png"
        return self.generate_image(prompt, path, "3:4")
    
    def generate_ugc_persona_image(self, persona_desc: str, 
                                    output_dir: str) -> str:
        """Gera imagem fotorrealista da persona para thumbnail do UGC."""
        prompt = f"""
        Photorealistic portrait of a Brazilian professional person.
        {persona_desc}
        Natural home office or coworking background, São Paulo aesthetic.
        Casual-professional attire, authentic expression looking at camera.
        Natural lighting, UGC style (not overly staged). 
        Smartphone or laptop subtly visible. High quality, 9:16 vertical.
        Do NOT include text overlays. Pure portrait for video thumbnail.
        """
        path = f"{output_dir}/ugc_persona_thumbnail.png"
        return self.generate_image(prompt, path, "9:16")
