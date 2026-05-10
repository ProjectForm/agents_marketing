from .base_agent import BaseAgent


class VideoScriptSpecialist(BaseAgent):
    agent_key = "video_script_specialist"

    def create_daily_video_package(self, theme: str, briefing: str) -> str:
        """
        Produces 1 complete UGC video production package (15-35s) for all platforms:
        YouTube Shorts, TikTok, Instagram Reels, Facebook.
        Includes scene-by-scene breakdown, narration, Veo context, platform adaptations.
        """
        prompt = f"""Crie o pacote completo de produção do vídeo UGC do dia.
1 vídeo que serve para: YouTube Shorts, TikTok, Instagram Reels e Facebook.
Duração total: 15-35 segundos (escolha a duração ideal para o tema).

TEMA: {theme}
BRIEFING: {briefing}

## VIDEO_MASTER
**Título do criativo:** [nome interno descritivo]
**Duração total:** [XX segundos]
**Número de clipes Veo:** [3 a 5 clipes — máx 7s cada]
**Pilar:** [educacional / engajamento / testemunho UGC]
**Persona:** [ex: designer freelancer SP, dev PJ BH, consultora MEI Curitiba]

## BRIEFING_PRODUCAO
**Cenário:** [ambiente, iluminação — ex: home office com janela lateral, luz natural]
**Roupa:** [casual profissional sem logos]
**Energia:** [ex: confidente e direto, empático, surpreso]
**Props:** [ex: celular na mesa, caneca — SEM tela visível]
**Câmera:** [selfie 9:16, altura dos olhos, steadicam ou apoio fixo]

## CENAS_DETALHADAS
Para cada clipe (máx 5 clipes × 7s = 35s):

**CLIPE 1 — GANCHO [0-7s]**
FALA: [texto exato para narração/legenda — máx 12 palavras]
AÇÃO NA TELA: [1 ação física simples — ex: olha pra câmera surpreso]
EMOÇÃO: [ex: surpresa, indignação, revelação]
VEO_CONTEXTO: [descrição cinemática 1-2 frases — SEM texto, SEM mãos em destaque, SEM tela de celular]

**CLIPE 2 — DESENVOLVIMENTO 1 [7-14s]**
FALA: [...]
AÇÃO NA TELA: [...]
EMOÇÃO: [...]
VEO_CONTEXTO: [...]

**CLIPE 3 — DESENVOLVIMENTO 2 [14-21s]**
FALA: [...]
AÇÃO NA TELA: [...]
EMOÇÃO: [...]
VEO_CONTEXTO: [...]

**CLIPE 4 — SOLUÇÃO [21-28s]**
FALA: [...]
AÇÃO NA TELA: [...]
EMOÇÃO: [...]
VEO_CONTEXTO: [...]

**CLIPE 5 — CTA [28-35s]**
FALA: [...]
AÇÃO NA TELA: [aponta para câmera ou sorri confiante]
EMOÇÃO: [confiante, convidativo]
VEO_CONTEXTO: [...]

## NARRACAO_COMPLETA
[Transcrição contínua de todos os clipes — o áudio completo do vídeo]

## TEXTO_OVERLAY_POR_PLATAFORMA
Textos para adicionar em edição (adicionados em pós-produção, NÃO pelo Veo):
- Instagram Reels: [texto overlay no gancho — máx 6 palavras]
- TikTok: [texto animado sugerido — máx 6 palavras]
- YouTube Shorts: [texto no gancho + texto no CTA]
- Facebook: [igual IG ou ajuste específico]

## TRILHA_SONORA
- Estilo: [ex: lo-fi leve, pop eletrônico sem letra, beats instrumentais]
- Energia: [calma / média / energética]
- Sugestão TikTok Sound: [tendência atual ou som original]
- Mixagem: [narração em destaque, música de fundo em 15-20% do volume]"""
        return self.run(prompt, reset_history=True)

    # ─── Legacy helpers para uso em weekly/monthly ────────────────────────────

    def create_reel_script(self, theme: str, briefing: str, duration_seconds: int = 30) -> str:
        prompt = f"""Roteiro para Reel (não UGC). TEMA: {theme} | Duração: {duration_seconds}s
Entregue: tipo de formato, cena-a-cena com timestamps, gancho nos primeiros 3s,
fala exata por cena, texto overlay, diretrizes de produção, sugestão de trilha."""
        return self.run(prompt, reset_history=True)

    def create_ugc_script(self, theme: str, briefing: str, persona_type: str = "") -> str:
        personas = {
            "designer": "Designer UI/UX freelancer, 27 anos, São Paulo",
            "dev": "Desenvolvedor web PJ, 33 anos, Belo Horizonte",
            "consultora": "Consultora de marketing autônoma, 35 anos, Curitiba",
            "fotografo": "Fotógrafo de eventos MEI, 30 anos, Recife",
        }
        persona = personas.get(persona_type, personas["designer"])
        prompt = f"""Roteiro UGC completo. TEMA: {theme} | PERSONA: {persona}
Estrutura: vida antes → problema → descoberta Finlancer → resultado → recomendação.
Tom: autêntico, conversacional, não propagandístico."""
        return self.run(prompt, reset_history=True)
