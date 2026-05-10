<!-- Aprovado pelo Brand Director em 2026-05-02 -->

## CARROSSEL

# CONCEITO VISUAL COMPLETO — CARROSSEL 8 SLIDES
## "Trabalhou sem contrato em 2025? Veja o que fazer antes do IRPF fechar em maio"
### Finlancer × Visual Creator | 02/05/2026

---

# PARTE 1 — PALETA DA PEÇA

```
┌─────────────────────────────────────────────────────────────────┐
│                     PALETA FINLANCER — IRPF EDITION             │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│   #0f172a    │   #1e293b    │   #10b981    │     #0ea5e9        │
│  Background  │   Surface    │   Emerald    │    Sky Blue        │
│   (fundo)    │   (cards)    │  (destaque)  │  (gradiente fim)   │
├──────────────┼──────────────┼──────────────┼────────────────────┤
│   #f1f5f9    │   #94a3b8    │   #f59e0b    │     #ef4444        │
│    Texto     │  Texto 2rio  │   Âmbar      │    Vermelho        │
│  Principal   │  (suporte)   │ (data/alerta)│ (só slide 3 — Pix) │
└──────────────┴──────────────┴──────────────┴────────────────────┘

GRADIENTE PRINCIPAL: linear-gradient(135deg, #10b981 → #0ea5e9)
GLOW EMERALD: box-shadow: 0 0 40px rgba(16,185,129,0.25)
GLASSMORPHISM: background: rgba(255,255,255,0.05) | blur(12px) | border: 1px solid rgba(255,255,255,0.08)
```

---

# PARTE 2 — WIREFRAMES SLIDE-A-SLIDE

---

## SLIDE 1 — CAPA
**Dimensão:** 1080 × 1350px

```
┌─────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  ← fundo #0f172a
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│                                         │
│         ┌─────────────────────┐         │  ← glow emerald radial
│         │  ╔═══════════════╗  │         │    rgba(16,185,129,0.15)
│         │  ║  [📄 ícone    ║  │         │    centro-baixo
│         │  ║   contrato]   ║  │         │
│         │  ║               ║  │         │  ← card glassmorphism
│         │  ║  [📅 31/mai]  ║  │         │    240×240px
│         │  ║   em emerald  ║  │         │    border-radius: 20px
│         │  ╚═══════════════╝  │         │
│         └─────────────────────┘         │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Cobrou sem contrato              │  │  ← Inter ExtraBold 64px
│  │  em 2025?                         │  │    #f1f5f9
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  O IRPF está te esperando.        │  │  ← Inter Regular 32px
│  └───────────────────────────────────┘  │    #10b981 (emerald)
│                                         │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← linha divisória
│                                         │    1px solid rgba(255,255,255,0.08)
│  [finlancer]              [→ deslize]   │  ← Inter Regular 22px
│   #10b981                  #94a3b8     │    logo + instrução nav
└─────────────────────────────────────────┘
```

**Especificações técnicas:**
| Elemento | Fonte | Tamanho | Cor | Posição |
|---|---|---|---|---|
| Título linha 1 | Inter ExtraBold | 64px | #f1f5f9 | x:72px, y:780px |
| Título linha 2 | Inter ExtraBold | 64px | #f1f5f9 | x:72px, y:860px |
| Subtítulo | Inter Regular | 32px | #10b981 | x:72px, y:960px |
| Card ícone | — | 240×240px | Glass | Centro, y:360px |
| Logo | Inter Bold | 26px | #10b981 | x:72px, y:1290px |
| "deslize" | Inter Regular | 22px | #94a3b8 | x:880px, y:1290px |

**Elemento decorativo:**
- Glow radial no canto inferior esquerdo: `radial-gradient(ellipse 600px 400px at 0% 100%, rgba(16,185,129,0.18), transparent)`
- Glow secundário centro: `radial-gradient(circle 300px at 50% 45%, rgba(16,185,129,0.08), transparent)`
- 3 pontos de "noise" — pequenos círculos rgba(16,185,129,0.06) espalhados no fundo

**Prompt Imagen 4 — Background/Elemento Visual:**
```
Dark tech abstract background, deep navy #0f172a, glowing emerald green document 
and calendar icons floating in glassmorphism card, soft radial glow emanating from 
bottom-left in emerald green, subtle particle dots scattered in dark space, 
cinematic dark UI aesthetic, 4K quality render, no text, no words, no letters, 
no hands, no people, no faces
```

---

## SLIDE 2 — RECONHECIMENTO
**Dimensão:** 1080 × 1350px

```
┌─────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  ← fundo #0f172a
│                                         │
│  [finlancer]                     [2/8]  │  ← header: logo + paginação
│   #10b981                    #94a3b8   │    y: 72px
│                                         │
│  ─────────────────────────────────────  │  ← linha 1px #10b981, y:120px
│                                         │
│         ┌─────────────────────┐         │
│         │                     │         │  ← ilustração centralizada
│         │   [silhueta humana  │         │    silhueta minimalista
│         │    com balão de     │         │    cor #1e293b fill
│         │    fala acima]      │         │    balão: glassmorphism
│         │                     │         │    ícone: 200×200px
│         └─────────────────────┘         │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ ╔═════════════════════════════╗ │    │  ← card glassmorphism
│  │ ║  Isso não é culpa sua.      ║ │    │    padding: 40px
│  │ ║                             ║ │    │    border-radius: 16px
│  │ ║  A maioria dos freelancers  ║ │    │
│  │ ║  começa assim: um Pix aqui, ║ │    │
│  │ ║  um acerto lá. Sem nota,    ║ │    │
│  │ ║  sem contrato, sem registro.║ │    │
│  │ ╚═════════════════════════════╝ │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  Não é irresponsabilidade —     │    │  ← Inter SemiBold 30px
│  │  é falta de estrutura.          │    │    #10b981
│  └─────────────────────────────────┘    │
│                                         │
│  O problema é o que fazer AGORA. ▸      │  ← Inter Regular 26px #94a3b8
│                                         │
└─────────────────────────────────────────┘
```

**Especificações técnicas:**
| Elemento | Fonte | Tamanho | Cor | Posição |
|---|---|---|---|---|
| Header logo | Inter Bold | 26px | #10b981 | x:72px, y:72px |
| Paginação | Inter Regular | 22px | #94a3b8 | x:960px, y:72px |
| Card principal | — | 936×480px | Glass | x:72px, y:540px |
| Texto card | Inter Regular | 32px | #f1f5f9 | dentro do card |
| Frase destaque | Inter SemiBold | 30px | #10b981 | x:72px, y:1120px |
| Gancho próx. | Inter Regular | 26px | #94a3b8 | x:72px, y:1220px |

**Elemento decorativo:**
- Silhueta humana abstrata: forma geométrica oval/retangular com bordas suaves, preenchimento `#1e293b`, posicionada centrada y:200-420px
- Balão de fala sobre a silhueta: card glassmorphism pequeno 180×60px com 3 pontos `#10b981` (loading style)
- Linha decorativa emerald: 1px horizontal, y:120px, largura 120px, x:72px

**Prompt Imagen 4 — Ilustração:**
```
Minimalist abstract human silhouette, dark navy background #0f172a, simple 
geometric person shape in dark slate color, small floating speech bubble element 
above in glassmorphism style with soft emerald glow, clean dark UI aesthetic, 
plenty of negative space, 4K quality, no text, no words, no letters, no hands 
visible, no detailed face
```

---

## SLIDE 3 — O PROBLEMA REAL
**Dimensão:** 1080 × 1350px

```
┌─────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  ← fundo #0f172a
│  [finlancer]                     [3/8]  │  ← header
│  ─────────────────────────────────────  │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  Quando você recebe um Pix      │    │  ← Inter ExtraBold 42px
│  │  por um serviço prestado...     │    │    #f1f5f9
│  └─────────────────────────────────┘    │
│                                         │
│  ┌──────────────────────────────────────┐│
│  │                                      ││  ← card fluxo visual
│  │  [ícone Pix]  ──────────▶  [ícone   ││    glassmorphism 936×200px
│  │   #10b981                   Receita] ││
│  │  "Recebimento"             "Registro"││
│  │   #f1f5f9 bold             #ef4444   ││  ← emerald → vermelho
│  └──────────────────────────────────────┘│    seta em gradiente
│                                          │
│  ┌─────────────────────────────────┐     │
│  │ ╔═══════════════════════════╗   │     │  ← card glassmorphism
│  │ ║  ...aquilo é renda.       ║   │     │    destaque
│  │ ║                           ║   │     │
│  │ ║  Não importa se foi no    ║   │     │
│  │ ║  Pix pessoal. Não importa ║   │     │
│  │ ║  se não teve nota. A      ║   │     │
│  │ ║  Receita Federal cruza    ║   │     │
│  │ ║  dados bancários.         ║   │     │
│  │ ╚═══════════════════════════╝   │     │
│  └─────────────────────────────────┘     │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ ⚠  E o prazo é 31 de maio.      │    │  ← badge alerta
│  └──────────────────────────────────┘    │    bg: rgba(245,158,11,0.12)
│                                          │    border: 1px solid #f59e0b
│                                          │    texto: #f59e0b Inter Bold 28px
└──────────────────────────────────────────┘
```

**Especificações técnicas:**
| Elemento | Fonte | Tamanho | Cor | Posição |
|---|---|---|---|---|
| Título | Inter ExtraBold | 42px | #f1f5f9 | x:72px, y:160px |
| Card fluxo | — | 936×200px | Glass | x:72px, y:380px |
| Ícone Pix label | Inter Bold | 28px | #10b981 | dentro do card, esq |
| Seta fluxo | — | 200px larg | grad. emer→verm | centro do card |
| Ícone Receita label | Inter Bold | 28px | #ef4444 | dentro do card, dir |
| Card texto | — | 936×340px | Glass | x:72px, y:640px |
| Texto card | Inter Regular | 30px | #f1f5f9 | dentro do card |
| Badge alerta | Inter Bold | 28px | #f59e0b | x:72px, y:1180px |

**Elemento decorativo:**
- A seta do fluxo Pix → Receita é um elemento gráfico com gradiente horizontal

---

## FEED

# CONCEITO VISUAL COMPLETO — POST FEED ESTÁTICO
## "31 de maio. Dois prazos. Uma decisão."
### Finlancer × Visual Creator | 02/05/2026

---

# DECISÃO DE FORMATO

**Escolha: 1080×1350px (4:5)**

**Justificativa:** O formato 4:5 ocupa 25% mais espaço no feed do que o quadrado. Para um post de urgência fiscal com data específica, essa metragem extra permite respiração entre os elementos sem comprometer a hierarquia. O eye-tracking no feed do Instagram favorece o 4:5 em conteúdo textual — o olho desce naturalmente de cima para baixo, e o CTA no rodapé tem mais chance de ser lido antes do scroll.

---

# CONCEITO CRIATIVO

## Ideia Central: "O Relógio Fiscal"

A peça comunica **urgência sem medo**. O elemento visual dominante é um contador regressivo estilizado — não um relógio de ansiedade, mas um marcador profissional e limpo que diz: *ainda dá tempo, mas o tempo está passando.*

A composição é dividida em três zonas verticais:

```
ZONA SUPERIOR (30%) → Elemento visual / urgência
ZONA CENTRAL (45%)  → Mensagem principal / hierarquia de texto
ZONA INFERIOR (25%) → Diferencial Finlancer + CTA
```

Essa divisão cria uma leitura em Z invertido — o olho entra pelo elemento visual, desce para o título, varre o subtítulo, e pousa no CTA.

---

# WIREFRAME DETALHADO

```
┌─────────────────────────────────────────────────────┐  1080px
│                                                     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← fundo #0f172a
│                                                     │
│  ═══════════════════════════════════════════════    │  ← linha decorativa
│                                          y: 60px    │  1px, #10b981, 80px larg
│                                                     │
│  ╔═══════════════════════════════════════════════╗  │  ← ZONA SUPERIOR
│  ║                                               ║  │    altura: 405px (30%)
│  ║         ┌────────────────────────┐            ║  │
│  ║         │  [elemento Imagen 4]   │            ║  │  ← imagem gerada
│  ║         │                        │            ║  │    480×320px
│  ║         │   glow abstrato com    │            ║  │    centralizada
│  ║         │   dois círculos        │            ║  │    border-radius: 20px
│  ║         │   emerald sobrepostos  │            ║  │
│  ║         │   + partículas         │            ║  │
│  ║         └────────────────────────┘            ║  │
│  ║                                               ║  │
│  ╚═══════════════════════════════════════════════╝  │
│                                                     │
│  ─────────────────────────────────────────────────  │  ← divisória
│                                          y: 465px   │    1px solid rgba(255,255,255,0.08)
│                                                     │
│  ╔═══════════════════════════════════════════════╗  │  ← ZONA CENTRAL
│  ║                                               ║  │    altura: 607px (45%)
│  ║                                               ║  │
│  ║   ┌───────────────────────────────────────┐   ║  │  ← badge data
│  ║   │  ⏱  31 de maio                        │   ║  │    glassmorphism pill
│  ║   └───────────────────────────────────────┘   ║  │    bg: rgba(245,158,11,0.10)
│  ║                                    y: 510px   ║  │    border: 1px solid #f59e0b
│  ║                                               ║  │    Inter Bold 24px #f59e0b
│  ║                                               ║  │    padding: 12px 24px
│  ║                                               ║  │    border-radius: 100px
│  ║   ┌───────────────────────────────────────┐   ║  │
│  ║   │  Dois prazos.                         │   ║  │  ← TÍTULO LINHA 1
│  ║   │  Uma decisão.                         │   ║  │    Inter ExtraBold 80px
│  ║   └───────────────────────────────────────┘   ║  │    #f1f5f9
│  ║                                    y: 590px   ║  │    line-height: 1.1
│  ║                                               ║  │
│  ║   ┌───────────────────────────────────────┐   ║  │  ← linha emerald
│  ║   │  ══════════════                       │   ║  │    4px height
│  ║   └───────────────────────────────────────┘   ║  │    #10b981
│  ║                                    y: 760px   ║  │    width: 64px
│  ║                                               ║  │
│  ║   ┌───────────────────────────────────────┐   ║  │  ← SUBTÍTULO
│  ║   │  IRPF fecha em 31/mai.                │   ║  │    Inter Regular 34px
│  ║   │  MEI Anual também.                    │   ║  │    #94a3b8
│  ║   │  Se você ainda não sabe               │   ║  │    line-height: 1.5
│  ║   │  como declarar o que recebeu          │   ║  │
│  ║   │  sem nota — ainda dá tempo.           │   ║  │
│  ║   └───────────────────────────────────────┘   ║  │
│  ║                                    y: 810px   ║  │
│  ║                                               ║  │
│  ╚═══════════════════════════════════════════════╝  │
│                                                     │
│  ─────────────────────────────────────────────────  │  ← divisória
│                                         y: 1072px   │    1px solid rgba(255,255,255,0.08)
│                                                     │
│  ╔═══════════════════════════════════════════════╗  │  ← ZONA INFERIOR
│  ║                                               ║  │    altura: 278px (25%)
│  ║                                               ║  │
│  ║   ┌───────────────────────────────────────┐   ║  │  ← card diferencial
│  ║   │ ╔═══════════════════════════════════╗ │   ║  │    glassmorphism
│  ║   │ ║  PF + PJ juntos, finalmente.      ║ │   ║  │    bg: rgba(16,185,129,0.08)
│  ║   │ ╚═══════════════════════════════════╝ │   ║  │    border: 1px solid rgba(16,185,129,0.25)
│  ║   └───────────────────────────────────────┘   ║  │    Inter SemiBold 28px #10b981
│  ║                                   y: 1110px   ║  │    border-radius: 12px
│  ║                                               ║  │    padding: 20px 28px
│  ║                                               ║  │
│  ║   [finlancer]          finlancer.com.br ▸     ║  │  ← rodapé
│  ║    Inter Bold 28px      Inter Regular 24px    ║  │    #10b981 / #94a3b8
│  ║                                   y: 1270px   ║  │
│  ║                                               ║  │
│  ╚═══════════════════════════════════════════════╝  │
│                                                     │
└─────────────────────────────────────────────────────┘
                                                 1350px
```

---

# ESPECIFICAÇÕES TIPOGRÁFICAS

```
┌──────────────────────────────────────────────────────────────────┐
│                    HIERARQUIA TIPOGRÁFICA                        │
├─────────────────┬──────────────────┬───────────┬────────────────┤
│    ELEMENTO     │      FONTE       │  TAMANHO  │      COR       │
├─────────────────┼──────────────────┼───────────┼────────────────┤
│ Badge data      │ Inter Bold       │   24px    │   #f59e0b      │
│ Título L1       │ Inter ExtraBold  │   80px    │   #f1f5f9      │
│ Título L2       │ Inter ExtraBold  │   80px    │   #f1f5f9      │
│ Subtítulo       │ Inter Regular    │   34px    │   #94a3b8      │
│ "ainda dá tempo"│ Inter SemiBold   │   34px    │   #f1f5f9      │
│ Card diferencial│ Inter SemiBold   │   28px    │   #10b981      │
│ Logo rodapé     │ Inter Bold       │   28px    │   #10b981      │
│ URL rodapé      │ Inter Regular    │   24px    │   #94a3b8      │
└─────────────────┴──────────────────┴───────────┴────────────────┘

LINE-HEIGHT: 1.1 para títulos | 1.5 para corpo
LETTER-SPACING: -0.02em para títulos grandes (tighten)
MARGEM LATERAL: 72px de cada lado (zona segura)
```

---

# PALETA DA PEÇA

```
┌──────────────────────────────────────────────────────────────────┐
│                      PALETA — FEED ESTÁTICO                      │
│                      "31 de maio. Dois prazos."                  │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│   #0f172a    │   #1e293b    │   #10b981    │     #f59e0b        │
│  Background  │  Card/Glass  │   Emerald    │      Amber         │
│  (base)      │  (surfaces)  │  (destaque   │   (urgência        │
│              │              │  primário)   │    de data)        │
├──────────────┼──────────────┼──────────────┼────────────────────┤
│   #f1f5f9    │   #94a3b8    │   #0ea5e9    │  rgba(16,185,      │
│  Texto prin. │  Texto secu. │  Sky (grad.) │   129, 0.08)       │
│  (títulos)   │  (subtítulo) │  (glow mix)  │  (tint emerald)    │
└──────────────┴──────────────┴──────────────┴────────────────────┘

NOTA SOBRE O AMBER (#f59e0b):
Usado exclusivamente no badge de data — cria tensão visual controlada
que sinaliza urgência sem alarmar. Contrasta com o emerald sem competir.
É a única cor quente da peça. Máximo 1 uso.

NOTA SOBRE O SKY (#0ea5e9):
Aparece apenas no glow do elemento Imagen 4 (zona superior),
mesclado ao emerald. Não é usado em texto.
```

---

# ELEMENTO VISUAL — ZONA SUPERIOR

## Conceito do Elemento Imagen 4

**O que é:** Dois círculos concêntricos sobrepostos de forma assimétrica — um maior em emerald, um menor em sky blue — representando visualmente os "dois prazos" do título. Cada círculo irradia um glow suave. Entre eles, partículas dispersas em escala de brilho decrescente. O conjunto flutua sobre fundo dark absoluto com profundidade criada por uma sombra radial.

**Por que funciona:** A abstração circular remete a contadores, timers, relógios — sem literalidade. Dois círculos = dois prazos. A assimetria intencional cria dinamismo. O glow emerald ancora na identidade Finlancer.

---

## Prompt Imagen 4 — VERSÃO PRINCIPAL

```
Two overlapping translucent circles, one large emerald green #10b981 glowing 
ring and one smaller sky blue #0ea5e9 glowing ring, asymmetric composition 
slightly offset, glassmorphism aesthetic on deep dark navy #0f172a background, 
soft radial glow emanating outward from each circle, scattered bright particles 
floating in dark space around the rings, cinematic 4K dark tech render, 
minimal and modern, no text, no words, no letters, no hands, no people, 
no faces, no logos
```

## Prompt Imagen 4 — VERSÃO ALTERNATIVA (se principal não satisfizer)

```
Abstract dark financial dashboard visualization, two luminous orbital rings 
in emerald green and sky blue overlapping on deep space dark navy background, 
glassmorphism glow effect, particle dust floating in negative space, 
premium dark SaaS aesthetic, centered composition with breathing room, 
ultra high definition render, no text, no words, no letters, no humans, 
no hands, no fingers
```

---

# COPY DA PEÇA

## Texto completo (camadas sobre o layout)

```
BADGE:     ⏱  31 de maio

TÍTULO:    Dois prazos.
           Uma decisão.

DIVISÓRIA: ████  (emerald, 4px × 64px)

SUBTÍTULO: IRPF fecha em 31/mai.
           MEI Anual também.
           Se você ainda não sabe como
           declarar o que recebeu sem
           nota — ainda dá tempo.

CARD:      PF + PJ juntos, finalmente.

RODAPÉ:    finlancer          finlancer.com.br ▸
```

**Nota de copy:** A frase "ainda dá tempo" está em `#f1f5f9` dentro do subtítulo em `#94a3b8` — o contraste intencional faz essa frase se destacar sem alterar o peso da fonte. É o ponto de virada emocional da peça: saiu do problema, entrou na solução.

---

# INSTRUÇÕES DE EXECUÇÃO NO CANVA

## Setup inicial

```
PASSO 1 — CRIAR O ARQUIVO
→ Canva Pro ou Canva gratuito
→ "Criar design" → "Tamanho personalizado"
→ Largura: 1080px | Altura: 1350px
→ Nome: "Feed_Finlancer_31maio