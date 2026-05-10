from .base_agent import BaseAgent


class SocialCopySpecialist(BaseAgent):
    agent_key = "social_copy_specialist"

    def create_full_copy_package(self, theme: str, briefing: str) -> str:
        """
        Produces the complete per-platform copy package.
        Output sections (all required):
          INSTAGRAM_LEGENDA, INSTAGRAM_CARROSSEL_TEXTOS, INSTAGRAM_ENGAGEMENT,
          TIKTOK_LEGENDA, TIKTOK_ENGAGEMENT, TIKTOK_VIDEO_IDEIA,
          YOUTUBE_LEGENDA, YOUTUBE_ENGAGEMENT,
          FACEBOOK_LEGENDA, FACEBOOK_STORYTELLING, FACEBOOK_ENGAGEMENT
        """
        prompt = f"""Crie o pacote completo de copy para hoje. Siga EXATAMENTE os cabeçalhos abaixo — todos são OBRIGATÓRIOS. Escreva o CONTEÚDO FINAL PRONTO, não templates ou instruções.

TEMA: {theme}
BRIEFING: {briefing}

---

## INSTAGRAM_LEGENDA
Escreva a legenda completa e final para o Reel do dia:
- 150-250 caracteres + 1 linha em branco + 4-6 hashtags relevantes
- Primeira linha = gancho que para o scroll (não comece com "Você sabia que")
- Segunda pessoa obrigatória ("você")
- CTA claro na última linha antes das hashtags
- Tom: como um MEI real falaria, sem "certamente", "fundamental", "é crucial"

## INSTAGRAM_CARROSSEL_TEXTOS
Escreva os textos FINAIS de cada um dos 8 slides (texto real, pronto para usar no Canva):

**SLIDE 1 — CAPA**
Título: [escreva o título aqui — máx 8 palavras]
Subtítulo: [escreva o subtítulo aqui — máx 12 palavras]

**SLIDE 2**
Título: [escreva o título aqui — máx 8 palavras]
Corpo: [escreva o corpo aqui — máx 20 palavras]

**SLIDE 3**
Título: [escreva o título aqui — máx 8 palavras]
Corpo: [escreva o corpo aqui — máx 20 palavras]

**SLIDE 4**
Título: [escreva o título aqui — máx 8 palavras]
Corpo: [escreva o corpo aqui — máx 20 palavras]

**SLIDE 5**
Título: [escreva o título aqui — máx 8 palavras]
Corpo: [escreva o corpo aqui — máx 20 palavras]

**SLIDE 6**
Título: [escreva o título aqui — máx 8 palavras]
Corpo: [escreva o corpo aqui — máx 20 palavras]

**SLIDE 7**
Título: [escreva o título aqui — máx 8 palavras]
Corpo: [escreva o corpo aqui — máx 20 palavras]

**SLIDE 8 — CTA**
Título: [escreva o CTA aqui — máx 8 palavras]
Corpo: [crie conta grátis no Finlancer — máx 15 palavras com finlancer.com.br]

## INSTAGRAM_ENGAGEMENT
- **Melhor horário para postar:** [dia específico + hora + 1 frase de justificativa]
- **Primeiro comentário a fixar:** [escreva o texto completo do comentário]
- **Pergunta para comentários:** [escreva a pergunta exata]
- **Stories após o post (sequência de 3):**
  - Story 1: [descrição do que postar]
  - Story 2: [descrição do que postar]
  - Story 3: [descrição do que postar]
- **Estratégia nas primeiras 2h:** [1 ação concreta e específica]

## TIKTOK_LEGENDA
Escreva a legenda final para TikTok (mais casual e direto que o Instagram):
- Máx 150 caracteres + 4-5 hashtags TikTok
- Tom descontraído, quase como mensagem de amigo
- Inclua 1 pergunta ou provocação que gera resposta nos comentários

## TIKTOK_ENGAGEMENT
- **Melhor horário TikTok:** [dia + hora específica]
- **Hashtags otimizadas:** [lista de 8-10 hashtags para o nicho MEI/freelancer]
- **Trend ou sound sugerido:** [nome específico de trend atual ou "som original" com justificativa]
- **Ideia de duet/stitch:** [conceito concreto — quem poderia fazer, sobre o quê]
- **Comentário fixado sugerido:** [texto completo]
- **Dica de algoritmo:** [1 ação concreta para distribuição orgânica]

## TIKTOK_VIDEO_IDEIA
Conceito completo de vídeo TikTok para o tema do dia:

**Formato:** [trend / tutorial / POV / stitch / talking head — escolha e justifique]
**Duração ideal:** [15s / 30s / 60s — justifique com base no conteúdo]
**Gancho visual (primeiros 2s):** [descreva o que aparece na tela nos primeiros 2 segundos]
**Roteiro em 3 atos:**
- Gancho: [fala exata de abertura — máx 10 palavras]
- Desenvolvimento: [o que acontece no meio — 2-3 frases]
- CTA: [chamada final — máx 8 palavras]
**Texto na tela:** [o que aparece como text overlay e em que momento]
**Som:** [nome da trend ou "som original" — justifique]
**Por que vai performar:** [1 razão concreta baseada no comportamento do público no TikTok]

## YOUTUBE_LEGENDA
**Título para YouTube Shorts:** [escreva o título completo — máx 60 caracteres, palavra-chave no início]
Ex de formato: "MEI e IRPF: o que fazer antes do prazo de maio"

**Descrição completa:**
[Escreva 3-5 linhas descrevendo o vídeo. Inclua:
- Linha 1: qual problema o vídeo resolve
- Linha 2: o que o espectador vai aprender
- Linha 3: CTA com finlancer.com.br
- Linha 4: hashtags (#MEI #IRPF #freelancer + 3 específicas do tema)]

**Tags para SEO:** [escreva 10 tags separadas por vírgula]
**Palavra-chave principal:** [1 termo de busca prioritário — ex: "declaração IRPF MEI 2026"]

## YOUTUBE_ENGAGEMENT
- **Conceito de thumbnail:** [descreva o que deve aparecer — expressão do criador, texto sobreposto em destaque, cor de fundo]
- **End screen CTA (últimos 3s):** [fala exata que o criador diz para fechar o vídeo]
- **Melhor horário de postagem:** [dia + hora]
- **Palavras-chave para SEO:** [lista de 5-8 termos prioritários de busca orgânica no YouTube]
- **Descrição da card/tela final:** [o que colocar como card no final para reter o espectador]

## FACEBOOK_LEGENDA
Caption completa para o vídeo no Facebook (100-200 palavras):
Mais contexto que o Instagram. Inclui link finlancer.com.br e CTA claro para criar conta.
Tom: narrativo, como alguém que entende do assunto mas fala simples.

## FACEBOOK_STORYTELLING
Post longo estilo storytelling (400-600 palavras):
Estrutura obrigatória:
1. Situação real de um MEI (use uma das personas: Fernanda, Lucas, Carla ou Rafael — sem citar o nome)
2. Problema específico que essa pessoa vivia
3. Como o Finlancer resolveu (funcionalidade real, não genérica)
4. Resultado concreto (com número se possível: "em 5 minutos", "R$ X economizados")
5. CTA: "Cria sua conta grátis em finlancer.com.br"
Tom: narrativo, empático, como se fosse o próprio usuário contando. Sem bullet points em excesso.

## FACEBOOK_ENGAGEMENT
- **Melhor horário Facebook:** [dia + hora]
- **Pergunta para gerar comentários:** [escreva a pergunta exata — deve gerar opinião, não resposta de sim/não]
- **Estratégia de boost:** [orgânico ou pago — justifique com base no tipo de conteúdo]
- **Segmentação sugerida se boost:** [público-alvo específico — faixa etária, interesse, localização]
- **Dica de engajamento:** [1 ação concreta nas primeiras 3h após postar]"""
        return self.run(prompt, reset_history=True)

    # ─── Helpers para planejamento semanal/mensal ─────────────────────────────

    def create_instagram_captions(self, theme: str, briefing: str) -> str:
        prompt = f"""Crie 4 legendas para Instagram.
TEMA: {theme} | BRIEFING: {briefing}
1. LEGENDA REEL — gancho + CTA + hashtags (150-250 chars)
2. LEGENDA CARROSSEL — gancho + CTA + hashtags
3. LEGENDA FEED ESTÁTICO — gancho + CTA + hashtags
4. LEGENDA STORIES — call-to-action direto"""
        return self.run(prompt, reset_history=True)

    def create_facebook_post(self, theme: str, briefing: str) -> str:
        prompt = f"""Post storytelling Facebook (400-600 palavras).
TEMA: {theme} | BRIEFING: {briefing}
Estrutura: Situação → Problema → Solução Finlancer → CTA com link."""
        return self.run(prompt)

    def create_carousel_texts(self, theme: str, num_slides: int, briefing: str) -> str:
        prompt = f"""Textos para carrossel de {num_slides} slides — TEMA: {theme}
BRIEFING: {briefing}
Cada slide: título (máx 8 palavras) + corpo (máx 20 palavras)."""
        return self.run(prompt)
