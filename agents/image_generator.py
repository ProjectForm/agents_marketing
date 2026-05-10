from google import genai
import os
from pathlib import Path
import time
import logging

logger = logging.getLogger("finlancer-agency")

NEGATIVE_PROMPT_IMAGEN = """
absolutely no text, no letters, no words, no captions, no writing,
no numbers, no watermarks, no logos, no typography of any kind,
pure visual composition only
"""

class ImageGeneratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "imagen-4.0-generate-001"
    
    def generate_image(self, prompt: str, output_path: str, 
                       aspect_ratio: str = "1:1", negative_prompt: str = "") -> str:
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
                negative_prompt=negative_prompt,
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
            logger.error(f"Erro ao gerar imagem para prompt \'{prompt[:50]}...\': {e}")
            return f"[ERRO_IMAGEM: {e}]"
    
    def generate_feed_image(self, theme: str, texto_overlay: str, 
                            output_dir: str) -> str:
        """
        Este método será substituído pelo VisualRenderer. Por enquanto, retorna um placeholder.
        """
        logger.info("ImageGeneratorAgent não gera mais imagens de feed diretamente. Usando VisualRenderer.")
        return "[PLACEHOLDER_FEED_IMAGE]"
    
    def generate_carousel_slide(self, slide_num: int, titulo: str, 
                                 corpo: str, output_dir: str) -> str:
        """
        Este método será substituído pelo VisualRenderer. Por enquanto, retorna um placeholder.
        """
        logger.info("ImageGeneratorAgent não gera mais slides de carrossel diretamente. Usando VisualRenderer.")
        return "[PLACEHOLDER_CAROUSEL_SLIDE]"
    
    def generate_ugc_persona_image(self, persona_desc: str, 
                                    output_dir: str, angle: str = "frontal") -> str:
        """
        Gera imagem fotorrealista da persona para thumbnail do UGC.
        angle: "frontal" ou "3/4"
        """
        prompt = f"""
        Photorealistic portrait of a Brazilian professional person.
        {persona_desc}
        Natural home office or coworking background, São Paulo aesthetic.
        Casual-professional attire, authentic expression looking at camera.
        Natural lighting, UGC style (not overly staged). 
        Smartphone or laptop subtly visible. High quality, 9:16 vertical.
        """
        if angle == "frontal":
            prompt += " Looking directly into camera, mouth slightly open, mid-conversation."
        elif angle == "3/4":
            prompt += " 3/4 angle, listening expression or hand near chin (vary posture)."

        path = f"{output_dir}/ugc_persona_thumbnail_{angle}.png"
        return self.generate_image(prompt, path, "9:16", negative_prompt=NEGATIVE_PROMPT_IMAGEN)
