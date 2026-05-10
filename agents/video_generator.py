from google import genai
import time
import os
import logging
from pathlib import Path

logger = logging.getLogger("finlancer-agency")

class VideoGeneratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "veo-3.1-lite-generate-preview"
    
    def generate_ugc_video(self, roteiro_pontos: list[str], 
                            persona_desc: str, output_dir: str) -> list[str]:
        """
        Gera 4 clipes de vídeo UGC com persona realista usando Veo 3.
        roteiro_pontos: lista de 4 pontos do roteiro (fala + ambientação)
        Retorna lista de paths dos MP4s salvos.
        """
        video_paths = []
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Garantir que temos 4 pontos
        while len(roteiro_pontos) < 4:
            roteiro_pontos.append("Ambientação: Escritório em casa. Fala: Continue acompanhando para mais dicas.")

        for i, ponto in enumerate(roteiro_pontos[:4]):
            video_prompt = f"""
            Short-form social media video clip (up to 7 seconds), vertical 9:16.
            
            CHARACTER: {persona_desc}
            A real-looking Brazilian professional speaking directly to camera.
            Casual home office setting, natural light, authentic UGC style.
            
            CLIP {i+1} CONTENT:
            {ponto}
            
            VISUAL STYLE:
            - Handheld feel (slight natural movement)
            - Warm natural lighting
            - Background: home office, plants, bookshelf
            - Character clothing: casual-professional
            
            MOOD: Authentic, relatable, trustworthy.
            No text overlays. No brand logos.
            """
            
            logger.info(f"Gerando clipe {i+1}/4 com prompt: {video_prompt[:100]}...")
            try:
                response = self.client.models.generate_videos(
                    model=self.model,
                    prompt=video_prompt,
                    config=genai.types.GenerateVideosConfig(
                        output_mime_type="video/mp4",
                        aspect_ratio="9:16",
                    )
                )

                operation = response
                while not operation.done:
                    logger.info(f"Aguardando conclusão do clipe {i+1}...")
                    time.sleep(10)
                    operation = self.client.operations.get(operation.name)
                
                if operation.error:
                    logger.error(f"Erro na geração do clipe {i+1}: {operation.error}")
                    continue

                video_data = operation.response.generated_videos[0].video.video_bytes
                output_path = Path(output_dir) / f"ugc_clip_{i+1}.mp4"
                with open(output_path, "wb") as f:
                    f.write(video_data)
                logger.info(f"Clipe {i+1} salvo em: {output_path}")
                video_paths.append(str(output_path))
                
                # Pequeno delay entre gerações para evitar rate limits
                if i < 3:
                    time.sleep(5)

            except Exception as e:
                logger.error(f"Erro ao gerar clipe {i+1}: {e}")
        
        return video_paths
