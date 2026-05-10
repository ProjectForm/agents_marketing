import json
import re

class OutputParser:
    def __init__(self):
        pass

    def generate_index_content(self, run_id, text_outputs, image_outputs, video_files, final_review, uploaded_drive_links=None):
        index_content = f"# Relatório de Produção de Conteúdo - {run_id}\n\n"
        index_content += f"## Revisão Final do Brand Director\n\n{final_review}\n\n"

        index_content += "## Outputs de Texto\n\n"
        for key, content in text_outputs.items():
            index_content += f"### {key.replace('_', ' ').title()}\n\n"
            if uploaded_drive_links and f'{key}.md' in uploaded_drive_links:
                index_content += f"[Ver no Google Drive]({uploaded_drive_links[f'{key}.md']})\n\n"
            index_content += f"```markdown\n{content}\n```\n\n"

        index_content += "## Outputs de Imagem\n\n"
        if image_outputs.get("feed_image_path"):
            index_content += f"### Imagem de Feed Estático\n\n"
            if uploaded_drive_links and 'feed_estatico.png' in uploaded_drive_links:
                index_content += f"[Ver no Google Drive]({uploaded_drive_links['feed_estatico.png']})\n\n"
            index_content += f"![Imagem de Feed]({image_outputs['feed_image_path']})\n\n"

        if image_outputs.get("carousel_images_paths"):
            index_content += f"### Carrossel de Imagens\n\n"
            for i, img_path in enumerate(image_outputs["carousel_images_paths"]):
                if uploaded_drive_links and f'carrossel_slide_{i+1:02d}.png' in uploaded_drive_links:
                    index_content += f"[Slide {i+1} no Google Drive]({uploaded_drive_links[f'carrossel_slide_{i+1:02d}.png']})\n\n"
                index_content += f"![Slide {i+1}]({img_path})\n\n"

        if image_outputs.get("ugc_persona_thumbnail_path"):
            index_content += f"### Thumbnail da Persona UGC\n\n"
            if uploaded_drive_links and 'ugc_persona_thumbnail.png' in uploaded_drive_links:
                index_content += f"[Ver no Google Drive]({uploaded_drive_links['ugc_persona_thumbnail.png']})\n\n"
            index_content += f"![Thumbnail Persona UGC]({image_outputs['ugc_persona_thumbnail_path']})\n\n"

        index_content += "## Outputs de Vídeo\n\n"
        if video_files:
            index_content += f"### Vídeo UGC\n\n"
            for i, video_path in enumerate(video_files):
                if uploaded_drive_links and f'ugc_video_clip_{i+1:02d}.mp4' in uploaded_drive_links:
                    index_content += f"[Clipe {i+1} no Google Drive]({uploaded_drive_links[f'ugc_video_clip_{i+1:02d}.mp4']})\n\n"
                index_content += f"[Download Clipe {i+1}]({video_path})\n\n"

        return index_content

    # The following methods are no longer needed as main.py directly parses the JSON output
    # def extract_feed_overlay_text(self, copy_output):
    #     # This method is now handled by directly accessing visual_output['feed_image']['overlay_text']
    #     pass

    # def extract_carousel_slides(self, visual_output):
    #     # This method is now handled by directly accessing visual_output['carousel']['slides']
    #     pass

    # def extract_ugc_persona_description(self, video_output):
    #     # This method is now handled by directly accessing visual_output['ugc_persona_image']['prompt']
    #     pass
