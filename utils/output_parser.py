import re
import json
from pathlib import Path

class OutputParser:
    
    def extract_carousel_slides(self, visual_output: str) -> list[dict]:
        """
        Lê o output do visual_content_creator.
        Pode ser uma string markdown ou um dicionário (se o agente retornou JSON).
        """
        slides = []
        
        # Se for um dicionário, tentar extrair da estrutura JSON
        if isinstance(visual_output, dict):
            carousel_data = visual_output.get("carousel", {})
            # O VisualContentCreator pode retornar uma string no campo 'concept'
            if isinstance(carousel_data, dict) and "concept" in carousel_data:
                concept_text = carousel_data["concept"]
                # Tentar parsear o concept_text se for JSON string
                try:
                    concept_json = json.loads(concept_text)
                    if "slides" in concept_json:
                        for s in concept_json["slides"]:
                            title = s.get("title", "")
                            body = s.get("subtitle", "") or s.get("body", "")
                            slides.append({"titulo": title, "corpo": body})
                except:
                    # Se falhar, tratar como texto normal abaixo
                    visual_output = concept_text
            else:
                visual_output = str(carousel_data)

        if not slides and isinstance(visual_output, str):
            # Tentar extrair do formato markdown gerado pelo OutputManager
            slide_blocks = re.findall(r"\*\*SLIDE (\d+).*?\*\*\n(.*?)(?=\n\*\*SLIDE|$)", visual_output, re.DOTALL)
            
            if not slide_blocks:
                # Fallback para o padrão do VisualContentCreator: "Slide X/8 — 1080x1350px"
                slide_blocks = re.findall(r"Slide (\d+)/8.*?\n(.*?)(?=\nSlide \d+/8|$)", visual_output, re.DOTALL)
            
            for num, block in slide_blocks:
                title_match = re.search(r'T[íi]tulo:\s*(.*?)(?=\n|$)', block) or re.search(r'Title:\s*(.*?)(?=\n|$)', block)
                body_match = re.search(r'Corpo:\s*(.*?)(?=\n|$)', block) or re.search(r'Subt[íi]tulo:\s*(.*?)(?=\n|$)', block) or re.search(r'Subtitle:\s*(.*?)(?=\n|$)', block)
                
                title = title_match.group(1).strip().strip('"') if title_match else ""
                body = body_match.group(1).strip().strip('"') if body_match else ""
                slides.append({"titulo": title, "corpo": body})
            
        # Garantir 8 slides
        while len(slides) < 8:
            slides.append({"titulo": "", "corpo": ""})
        return slides[:8]
    
    def extract_feed_overlay_text(self, copy_output: str) -> str:
        """
        Extrai o título/gancho principal da LEGENDA 4 (FEED ESTÁTICO).
        """
        # Tentar encontrar a seção LEGENDA 4
        section_match = re.search(r"LEGENDA 4.*?(?=\n## |$)", copy_output, re.DOTALL | re.IGNORECASE)
        if section_match:
            section = section_match.group(0)
            # Tentar encontrar o gancho/título dentro da seção
            match = re.search(r"GANCHO/T[Íi]TULO:\s*(.*?)(?=\n|$)", section, re.IGNORECASE)
            if match:
                return match.group(1).strip().strip('"')
            # Fallback: primeira linha não vazia após o cabeçalho da seção
            lines = [l.strip() for l in section.split('\n') if l.strip() and 'LEGENDA 4' not in l]
            if lines:
                return lines[0].strip().strip('"')
        return ""
    
    def extract_ugc_persona_description(self, video_output: str) -> str:
        """
        Extrai a descrição da persona do roteiro UGC.
        """
        # Padrão: "PERSONA: ..."
        match = re.search(r"PERSONA:\s*(.*?)(?=\n|$)", video_output, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return "A Brazilian professional freelancer, authentic and relatable."

    def generate_index_content(self, run_id: str, text_outputs: dict, image_outputs: dict, final_review: str, uploaded_drive_links: dict) -> str:
        """
        Gera o conteúdo do INDEX.md com links do Drive.
        """
        links_str = ""
        for name, link in uploaded_drive_links.items():
            links_str += f"- **{name.replace('_', ' ').title()}**: [Acessar no Drive]({link})\n"
            
        return f"""# Pacote de Conteúdo Finlancer - {run_id}

Este pacote contém todos os entregáveis gerados automaticamente pelos agentes para a rotina de hoje.

## 📁 Arquivos no Google Drive
{links_str}

## 📝 Resumo Estratégico (Brand Director)
{final_review}

## 🚀 Próximos Passos
1. Revise as legendas e artes no link acima.
2. Agende as postagens conforme o cronograma.
3. Monitore o engajamento!

---
*Gerado automaticamente pela Agência Finlancer (Gemini 2.5 + Imagen 4 + Veo 3)*
"""
