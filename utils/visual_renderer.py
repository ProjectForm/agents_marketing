import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path
import logging

logger = logging.getLogger("finlancer-agency")

class VisualRenderer:
    def __init__(self):
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
        if not self.pexels_api_key:
            logger.warning("PEXELS_API_KEY not found. Pexels image search will be mocked.")

        # Definir paleta de cores
        self.colors = {
            "emerald_primary": "#10B981",
            "emerald_dark": "#0F5132",
            "emerald_medium": "#16A34A",
            "text_body": "#1A1A1A",
            "text_on_emerald": "#FFFFFF",
            "background_paper": "#F5F2EA",
            "background_mint": "#D9F2EE",
        }

        # Definir fontes (assumindo que estão disponíveis ou serão carregadas)
        # Para simplificar, usaremos fontes padrão ou precisaremos de um mecanismo para carregá-las
        # Exemplo: self.font_bold = ImageFont.truetype("path/to/bold_font.ttf", size)
        # Por enquanto, usaremos o default do Pillow

    def _get_font(self, size, weight="regular"):
        # Placeholder para carregamento de fontes. Em um ambiente real, você carregaria .ttf
        try:
            if weight == "bold":
                return ImageFont.truetype("arialbd.ttf", size) # Exemplo de fonte bold
            return ImageFont.truetype("arial.ttf", size) # Exemplo de fonte regular
        except IOError:
            logger.warning(f"Font not found for weight {weight}. Using default Pillow font.")
            return ImageFont.load_default()

    def search_pexels_image(self, query: str, orientation: str = "landscape") -> str:
        if not self.pexels_api_key:
            logger.info(f"[MOCK] Searching Pexels for: {query}")
            return "https://via.placeholder.com/1920x1080.png?text=Pexels+Mock+Image"

        headers = {"Authorization": self.pexels_api_key}
        params = {"query": query, "orientation": orientation, "per_page": 1}
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["original"]
        return ""

    def download_image(self, url: str) -> Image.Image:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))

    def create_feed_image(self, title: str, illustration_prompt: str, style: str, output_path: Path) -> Path:
        # Implementar lógica para Sub-estilo A (Curiosidade visual) e B (Hook de texto puro)
        # Por enquanto, um placeholder simples
        img = Image.new('RGB', (1080, 1080), color=self.colors["background_paper"])
        d = ImageDraw.Draw(img)
        font = self._get_font(50, "bold")
        d.text((50, 50), title, fill=self.colors["text_body"], font=font)
        img.save(output_path)
        logger.info(f"Feed image saved to {output_path}")
        return output_path

    def create_carousel_slide(self, slide_data: dict, background_image_url: str, output_path: Path) -> Path:
        # Implementar lógica para sobrepor texto e caixa emerald sobre imagem Pexels
        # Por enquanto, um placeholder simples
        bg_img = self.download_image(background_image_url).resize((1080, 1350))
        img = bg_img.copy()
        d = ImageDraw.Draw(img)
        font_title = self._get_font(60, "bold")
        font_body = self._get_font(30)
        d.text((50, 50), slide_data.get("titulo", ""), fill=self.colors["text_on_emerald"], font=font_title)
        d.text((50, 150), slide_data.get("corpo", ""), fill=self.colors["text_body"], font=font_body)
        img.save(output_path)
        logger.info(f"Carousel slide saved to {output_path}")
        return output_path

    def create_ugc_persona_thumbnail(self, persona_prompt: str, output_path: Path) -> Path:
        # Usar Imagen 4 para gerar a thumbnail da persona
        # Esta lógica será movida para ImageGeneratorAgent, que chamará este método para salvar
        # Por enquanto, um placeholder
        img = Image.new('RGB', (1080, 1920), color=self.colors["background_mint"])
        d = ImageDraw.Draw(img)
        font = self._get_font(50)
        d.text((50, 50), "UGC Persona Thumbnail", fill=self.colors["text_body"], font=font)
        img.save(output_path)
        logger.info(f"UGC persona thumbnail saved to {output_path}")
        return output_path
