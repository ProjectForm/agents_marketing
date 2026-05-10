<!-- Aprovado pelo Brand Director em 2026-05-02 -->

## CARROSSEL

# CONCEITO VISUAL COMPLETO — CARROSSEL 8 SLIDES
## Finlancer × IRPF + MEI Anual — 02/05/2026

> **Nota:** O briefing especifica 7 slides. Expandi para 8 conforme solicitado na tarefa. O slide extra (S8 no briefing = S7 original + CTA reforçado) funciona como encerramento com logo.

---

## ━━━ PALETA DA PEÇA ━━━

```
BACKGROUNDS
├── Base:        #0f172a  — fundo principal todos os slides
├── Surface:     #1e293b  — cards e containers
└── Surface+:    #334155  — elementos elevados / hover state

TEXTO
├── Primário:    #f1f5f9  — títulos e corpo principal
├── Secundário:  #94a3b8  — labels, legendas, texto de suporte
└── Inverso:     #0f172a  — texto sobre botão emerald

ACCENT (INEGOCIÁVEL)
├── Emerald:     #10b981  — CTAs, destaques, bordas ativas, ícones
├── Emerald Dark:#059669  — profundidade em gradientes
└── Emerald Light:#34d399 — highlights, micro-detalhes

GRADIENTE PRINCIPAL
└── #10b981 → #0ea5e9  — usar em elementos de destaque máximo

GLASSMORPHISM
├── Fill:        rgba(30, 41, 59, 0.7)   — cards com blur
├── Border:      rgba(255, 255, 255, 0.08) — borda sutil
└── Glow:        rgba(16, 185, 129, 0.15) — sombra emerald
```

---

## ━━━ SISTEMA DE DESIGN DA PEÇA ━━━

### Fio Condutor Visual
**O Duo de Cards PF + PJ** — aparece em todos os slides em alguma forma. A metáfora visual central: dois mundos financeiros que o Finlancer une. O card PF tem borda **#0ea5e9 (sky blue)**, o card PJ tem borda **#10b981 (emerald)**. Quando se fundem (S5+), a borda vira gradiente dos dois.

### Grid Base (1080×1350px)
```
Margem lateral:    72px cada lado  →  área útil: 936px
Zona superior:     120px           →  espaço para respirar
Zona inferior:     120px           →  CTA / disclaimer
Calha interna:     24px entre colunas
```

### Tipografia — Sistema
```
Display (números grandes):  Inter ExtraBold 800 — 96-120px
H1 (título capa):           Inter ExtraBold 800 — 72px
H2 (título slides internos): Inter Bold 700 — 52px
H3 (subtítulo / label):     Inter SemiBold 600 — 28px
Body (texto explicativo):   Inter Regular 400 — 28-32px
Caption / disclaimer:       Inter Regular 400 — 20px — #94a3b8
Número de slide:            Inter Medium 500 — 18px — #94a3b8
```

### Bordas e Raios
```
Cards grandes:    border-radius 20px
Cards menores:    border-radius 14px
Botão CTA:        border-radius 12px
Pílulas/badges:   border-radius 100px (pill shape)
```

---

## ━━━ WIREFRAMES SLIDE A SLIDE ━━━

---

### 🔲 SLIDE 1 — CAPA
**Função:** Parar o scroll. Impacto máximo em 2 segundos.

```
┌─────────────────────────────────────┐  1080×1350px
│  fundo: #0f172a                      │
│                                      │
│   ···· partículas emerald sutis ···  │ y: 0-200px
│                                      │
│  ┌──────────────────────────────┐    │
│  │ CARD PJ  (emerald border)    │    │ card sobreposto
│  │ background: rgba(30,41,59,.7)│    │ y: 180px
│  │ border: #10b981 1px          │    │ w: 800px h: 220px
│  │ border-radius: 20px          │    │
│  │  ● CNPJ                      │    │
│  │  faturamento  R$ 47.320      │    │
│  └──────────────────────────────┘    │
│     ┌──────────────────────────────┐ │
│     │ CARD PF  (sky border)        │ │ offset: +40px X, +40px Y
│     │ border: #0ea5e9 1px          │ │ y: 220px
│     │ border-radius: 20px          │ │
│     │  ● CPF                       │ │
│     │  renda     R$ 54.800         │ │
│     └──────────────────────────────┘ │
│                                      │
│  ┌──── BADGE URGÊNCIA ────────────┐  │ y: 500px
│  │  ⏰  31/maio  ←  pill emerald  │  │ pill: bg #10b981 text #0f172a
│  └───────────────────────────────┘   │ bold 22px
│                                      │
│  TÍTULO H1 (duas linhas):            │ y: 580px
│  ┌──────────────────────────────┐    │
│  │ MEI e IRPF vencem          │    │ 72px ExtraBold #f1f5f9
│  │ no mesmo dia.               │    │ line-height: 1.15
│  └──────────────────────────────┘    │
│                                      │
│  SUBTÍTULO:                          │ y: 780px
│  Você sabe o que fazer com os dois?  │ 32px Regular #94a3b8
│                                      │
│  ─────── linha emerald 2px ───────   │ y: 900px w: 120px
│                                      │
│  ○ deslize para ver o passo a passo  │ y: 940px 22px #94a3b8
│                                      │
│  [finlancer]  ←  logo bottom right  │ y: 1270px x: 900px
└─────────────────────────────────────┘
```

**Elemento decorativo:**
Círculo de glow emerald `rgba(16,185,129,0.12)` com `filter: blur(80px)` posicionado atrás dos cards, centro em x:540 y:360. Raio: 400px. Cria profundidade sem poluição.

**Especificações dos Cards sobrepostos:**
- Card PJ: `x:140 y:180 w:800 h:220` — borda `#10b981` 1.5px
- Card PF: `x:180 y:260 w:800 h:220` — borda `#0ea5e9` 1.5px — `z-index` abaixo
- Efeito de sombra card PJ: `box-shadow: 0 20px 40px rgba(16,185,129,0.20)`

---

### 🔲 SLIDE 2 — CONTEXTUALIZAÇÃO
**Função:** Explicar que são duas obrigações distintas — muita gente confunde.

```
┌─────────────────────────────────────┐  1080×1350px
│  fundo: #0f172a                      │
│                                      │
│  NÚMERO DO SLIDE:  02/08             │ y: 60px x: 972px
│                                      │
│  LABEL SUPERIOR:                     │ y: 100px
│  [  DUAS OBRIGAÇÕES. UM PRAZO.  ]   │ pill: bg #1e293b border #10b981
│                                      │ text: #10b981 24px SemiBold
│                                      │
│  TÍTULO H2:                          │ y: 200px
│  Não é a mesma coisa.               │ 64px ExtraBold #f1f5f9
│                                      │
│  LINHA DIVISÓRIA EMERALD             │ y: 295px w: 80px h: 3px #10b981
│                                      │
│  ┌─────────────┐   ┌─────────────┐  │ y: 360px
│  │  COLUNA PF  │   │  COLUNA PJ  │  │
│  │ ─────────── │   │ ─────────── │  │
│  │  IRPF       │   │ DASN-SIMEI  │  │ dois cards lado a lado
│  │             │   │             │  │ cada: w:440 h:520
│  │  Declara-   │   │  Declaração │  │ border-radius: 20px
│  │  ção da     │   │  do MEI     │  │ bg: rgba(30,41,59,0.7)
│  │  pessoa     │   │  para a     │  │
│  │  física     │   │  Receita    │  │
│  │             │   │  Federal    │  │
│  │  ↑ toda     │   │  ↑ obrigat. │  │
│  │  renda PF   │   │  se faturou │  │
│  │  + rendim.  │   │  qualquer   │  │
│  │  do CNPJ    │   │  valor      │  │
│  │             │   │             │  │
│  │ border:     │   │ border:     │  │
│  │ #0ea5e9     │   │ #10b981     │  │
│  └─────────────┘   └─────────────┘  │
│                                      │
│  ┌──────────────────────────────┐    │ y: 980px
│  │ Ambas vencem em 31 de maio.  │    │ bg: rgba(16,185,129,0.10)
│  │ Precisam de dados diferentes.│    │ border-left: 4px #10b981
│  └──────────────────────────────┘    │ padding: 20px 24px
│                                      │
│  [finlancer]                         │ y: 1290px x: 900px
└─────────────────────────────────────┘
```

**Elemento decorativo:**
Linha vertical central emerald `#10b981` com 2px largura e `opacity: 0.3`, do topo ao fundo dos cards — reforça a divisão visual PF × PJ.

**Detalhe dos cards-coluna:**
- Ícone no topo de cada card: círculo 48px — PF em `#0ea5e9`, PJ em `#10b981`
- Texto dos cards: Inter Regular 26px `#f1f5f9` com labels em SemiBold 28px

---

### 🔲 SLIDE 3 — OBRIGAÇÃO 1: IRPF
**Função:** Explicar o que o MEI precisa declarar no IRPF.

```
┌─────────────────────────────────────┐  1080×1350px
│  fundo: #0f172a                      │
│                                      │
│  NÚMERO DO SLIDE:  03/08             │ y: 60px x: 972px
│                                      │
│  LABEL:  [ IRPF — PESSOA FÍSICA ]   │ y: 100px pill sky blue
│  bg: rgba(14,165,233,0.15) border: #0ea5e9  text: #0ea5e9
│                                      │
│  TÍTULO H2:                          │ y: 180px
│  O que o MEI declara                │ 56px ExtraBold #f1f5f9
│  no IRPF?                           │ line-height: 1.2
│                                      │
│  ┌──── CARD MOCK IRPF ────────────┐  │ y: 360px
│  │  glassmorphism card            │  │ w: 936px h: 580px
│  │  bg: rgba(30,41,59,0.8)        │  │ border: rgba(14,165,233,0.3)
│  │  border-radius: 20px           │  │
│  │                                │  │
│  │  SEÇÃO: RENDIMENTOS TRIBUTÁVEIS│  │ label 20px #94a3b8
│  │  ──────────────────────────── │  │ divider 1px rgba(255,255,255,0.06)
│  │  Salário / freela PF   R$ 0    │  │ 28px Regular #f1f5f9
│  │  Aluguéis              R$ 0    │  │
│  │                                │  │
│  │  SEÇÃO: RENDIMENTOS ISENTOS    │  │ label 20px #94a3b8
│  │  ──────────────────────────── │  │
│  │  Lucro distribuído MEI R$ 44.200│ │ 28px Regular #f1f5f9
│  │  (desde que dentro do limite)  │  │ 22px #94a3b8 italic
│  │                                │  │
│  │  SEÇÃO: BENS E DIREITOS        │  │
│  │  ──────────────────────────── │  │
│  │  CNPJ (MEI)      ✓ incluir     │  │ emerald check icon
│  └────────────────────────────────┘  │
│                                      │
│  ┌──────────────────────────────┐    │ y: 1020px
│  │ ⚡ O lucro do MEI vai no IRPF │    │ bg: rgba(16,185,129,0.10)
│  │ como rendimento isento.      │    │ border-left: 4px #10b981
│  │ Mas precisa estar separado.  │    │ 26px Regular #f1f5f9
│  └──────────────────────────────┘    │
│                                      │
│  [finlancer]                         │ y: 1290px x: 900px
└─────────────────────────────────────┘
```

**Detalhes visuais específicos:**
- O card IRPF usa borda `#0ea5e9` (sky blue, cor PF) para reforçar o sistema de cores
- Os valores simulados devem parecer reais: R$ 44.200 (não número redondo)
- Ícone de check `✓` em emerald antes de "CNPJ (MEI)" — mini-ícone circular 24px

---

### 🔲 SLIDE 4 — OBRIGAÇÃO 2: DASN-SIMEI
**Função:** Explicar o MEI Anual — o que é, quem precisa entregar.

---

## FEED

# CONCEITO VISUAL — POST FEED ESTÁTICO
## Finlancer × IRPF + MEI Anual — 02/05/2026

---

## ━━━ DECISÃO DE FORMATO ━━━

**Formato escolhido: 1080×1080px (1:1)**

**Justificativa:** Para um post estático isolado com tema de urgência suave, o quadrado funciona melhor. A composição simétrica de dois cards lado a lado — PF × PJ — encaixa naturalmente no formato 1:1 sem forçar espaço vertical. O impacto visual é imediato no feed sem precisar de scroll.

---

## ━━━ PALETA DA PEÇA ━━━

```
┌─────────────────────────────────────────────────────────┐
│  CORES DA PEÇA                                          │
│                                                         │
│  ■ #0f172a   Background principal — Slate 900           │
│  ■ #1e293b   Surface dos cards — Slate 800              │
│  ■ #334155   Borda elevada / detalhe — Slate 700        │
│                                                         │
│  ■ #10b981   Emerald — accent, destaque, CTA            │
│  ■ #059669   Emerald Dark — profundidade/gradiente      │
│  ■ #0ea5e9   Sky Blue — cor do mundo PF                 │
│                                                         │
│  ■ #f1f5f9   Texto primário — Slate 100                 │
│  ■ #94a3b8   Texto secundário — Slate 400               │
│                                                         │
│  GRADIENTE ACCENT:  #10b981 → #0ea5e9  (135deg)        │
│  GLOW EMERALD:      rgba(16, 185, 129, 0.18)            │
│  GLOW SKY:          rgba(14, 165, 233, 0.18)            │
└─────────────────────────────────────────────────────────┘
```

---

## ━━━ CONCEITO CRIATIVO ━━━

**Nome interno:** *"Dois Mundos, Um Prazo"*

**Ideia central:**
A imagem comunica em 2 segundos o que o copy vai explicar: você tem **dois universos financeiros separados** (PF e PJ) e **um único prazo que os une** (31/maio). A tensão visual entre separação e convergência É a mensagem.

**Metáfora visual:**
Dois cards glassmorphism — um em sky blue (PF/pessoa física), outro em emerald (PJ/MEI) — posicionados como espelhos um do outro, separados por uma linha central de gradiente. No centro, um badge com "31/maio" em destaque máximo. Os dois cards "apontam" para ele.

---

## ━━━ WIREFRAME DETALHADO ━━━

```
┌────────────────────────────────────────────────┐
│  1080 × 1080 px  —  background: #0f172a        │
│                                                 │
│  ┌── GLOW ESQUERDO ──────────────────────────┐ │
│  │  circle: 380px  blur: 100px               │ │
│  │  color: rgba(14,165,233,0.12)             │ │
│  │  center: x:200 y:540                      │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌── GLOW DIREITO ───────────────────────────┐ │
│  │  circle: 380px  blur: 100px               │ │
│  │  color: rgba(16,185,129,0.12)             │ │
│  │  center: x:880 y:540                      │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ──── ZONA SUPERIOR (y: 60-160px) ─────────── │
│                                                 │
│  [  MAIO 2026  ]   ←  pill badge               │
│   x:396 y:72 w:288 h:40                        │
│   bg: rgba(16,185,129,0.12)                    │
│   border: 1px solid #10b981                    │
│   text: #10b981  Inter SemiBold 18px           │
│   border-radius: 100px                         │
│                                                 │
│  ──── ZONA TÍTULO (y: 150-280px) ──────────── │
│                                                 │
│  TÍTULO LINHA 1:                               │
│  "Dois prazos."                                │
│   x:80  y:155  w:920                           │
│   Inter ExtraBold 800  72px                    │
│   color: #f1f5f9   text-align: center          │
│                                                 │
│  TÍTULO LINHA 2 (gradient text):               │
│  "Uma bagunça."                                │
│   x:80  y:238  w:920                           │
│   Inter ExtraBold 800  72px                    │
│   fill: gradient #10b981→#0ea5e9               │
│   text-align: center                           │
│                                                 │
│  ──── ZONA CARDS (y: 310-760px) ───────────── │
│                                                 │
│  ┌─────────────────────┐   ┌─────────────────┐│
│  │  CARD ESQUERDO: PF  │   │  CARD DIREITO:  ││
│  │                     │   │       PJ        ││
│  │  x:60  y:310        │   │  x:572  y:310   ││
│  │  w:448  h:450       │   │  w:448  h:450   ││
│  │  border-radius: 20px│   │  border-r: 20px ││
│  │  bg: rgba(30,41,59  │   │  bg: rgba(30,41 ││
│  │       ,0.75)        │   │       ,59,0.75) ││
│  │  border: 1.5px      │   │  border: 1.5px  ││
│  │  #0ea5e9            │   │  #10b981        ││
│  │  backdrop-blur: 12px│   │  backdrop-blur  ││
│  │                     │   │        :12px    ││
│  │  ┌─ HEADER ───────┐ │   │  ┌─ HEADER ───┐ ││
│  │  │ ● CPF          │ │   │  │ ● CNPJ     │ ││
│  │  │ icon: sky blue │ │   │  │ icon: emrld│ ││
│  │  │ 22px SemiBold  │ │   │  │ 22px SmBld │ ││
│  │  └────────────────┘ │   │  └────────────┘ ││
│  │                     │   │                 ││
│  │  LABEL:             │   │  LABEL:         ││
│  │  "IRPF"             │   │  "MEI Anual"    ││
│  │  Inter Bold 36px    │   │  Inter Bold 36px││
│  │  #f1f5f9            │   │  #f1f5f9        ││
│  │                     │   │                 ││
│  │  ─── divider 1px ── │   │  ─── divider ── ││
│  │  rgba(255,255,255   │   │  rgba(255,255,  ││
│  │       ,0.08)        │   │       255,0.08) ││
│  │                     │   │                 ││
│  │  "Declaração da"    │   │  "Declaração do"││
│  │  "pessoa física"    │   │  "faturamento"  ││
│  │  Inter Reg 22px     │   │  Inter Reg 22px ││
│  │  #94a3b8            │   │  #94a3b8        ││
│  │                     │   │                 ││
│  │  ─── NÚMERO ──────  │   │  ─── NÚMERO ─── ││
│  │  R$ 54.800          │   │  R$ 47.320      ││
│  │  Inter ExBld 48px   │   │  Inter ExBld48px││
│  │  #0ea5e9            │   │  #10b981        ││
│  │                     │   │                 ││
│  │  "renda declarada"  │   │  "faturamento"  ││
│  │  22px #94a3b8       │   │  22px #94a3b8   ││
│  └─────────────────────┘   └─────────────────┘│
│                                                 │
│  ──── BADGE CENTRAL (y: 502px) ─────────────── │
│                                                 │
│        ┌──────────────────────┐                 │
│        │   ⏰  31/maio        │                 │
│        │                      │                 │
│        │  x:366  y:502        │                 │
│        │  w:348  h:56         │                 │
│        │  bg: #10b981         │                 │
│        │  border-radius: 12px │                 │
│        │  text: #0f172a       │                 │
│        │  Inter ExBold 28px   │                 │
│        │  shadow: 0 0 24px    │                 │
│        │  rgba(16,185,129,.4) │                 │
│        └──────────────────────┘                 │
│        (badge sobrepõe os dois cards no centro) │
│                                                 │
│  ──── LINHA SEPARADORA GRADIENTE ──────────── │
│                                                 │
│  linha vertical central: x:540                 │
│  y:300  h:470  w:2px                           │
│  gradient: #0ea5e9 → #10b981  (top→bottom)    │
│  opacity: 0.5                                  │
│                                                 │
│  ──── ZONA COPY INFERIOR (y: 790-920px) ────── │
│                                                 │
│  SUBTÍTULO PRINCIPAL:                          │
│  "Os dois vencem em 31/maio."                  │
│   x:80 y:800 w:920                             │
│   Inter Bold 32px  #f1f5f9  text-align: center │
│                                                 │
│  BODY:                                         │
│  "Você sabe o que precisa fazer em cada um?"   │
│   x:80  y:852  w:920                           │
│   Inter Regular 26px  #94a3b8  text-align:center│
│                                                 │
│  ──── ZONA CTA (y: 940-1020px) ─────────────── │
│                                                 │
│  ┌──── BOTÃO CTA ────────────────────────────┐ │
│  │  Veja o carrossel →                       │ │
│  │  x:340  y:940  w:400  h:56                │ │
│  │  bg: rgba(16,185,129,0.15)                │ │
│  │  border: 1.5px solid #10b981              │ │
│  │  border-radius: 12px                      │ │
│  │  text: #10b981  Inter SemiBold 22px       │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ──── RODAPÉ (y: 1034-1060px) ──────────────── │
│                                                 │
│  [finlancer]  ←  logo                          │
│   x:440  y:1040  h:28px                        │
│   color: #f1f5f9  Inter ExtraBold              │
│                                                 │
│  "finlancer.com.br"                            │
│   x:440  y:1058                                │
│   color: #94a3b8  Inter Regular 16px           │
└────────────────────────────────────────────────┘
```

---

## ━━━ COPY DA PEÇA ━━━

```
BADGE SUPERIOR:
"MAIO 2026"

TÍTULO LINHA 1 (branco):
"Dois prazos."

TÍTULO LINHA 2 (gradient emerald→sky):
"Uma bagunça."

CARD ESQUERDO — PF (sky blue #0ea5e9):
Header:    ● CPF
Label:     IRPF
Descrição: Declaração da pessoa física
Número:    R$ 54.800
Sublabel:  renda declarada

CARD DIREITO — PJ (emerald #10b981):
Header:    ● CNPJ
Label:     MEI Anual
Descrição: Declaração do faturamento
Número:    R$ 47.320
Sublabel:  faturamento

BADGE CENTRAL:
⏰ 31/maio

SUBTÍTULO:
"Os dois vencem em 31/maio."

BODY:
"Você sabe o que precisa fazer em cada um?"

BOTÃO:
"Veja o carrossel →"

RODAPÉ:
finlancer
finlancer.com.br
```

**Contagem de texto:** 7 palavras no título principal (dentro do limite de 8) ✅
**Subtítulo:** 7 palavras (dentro do limite de 12) ✅

---

## ━━━ HIERARQUIA VISUAL — ORDEM DE LEITURA ━━━

```
① Badge "MAIO 2026"     →  âncora temporal, contexto imediato
② "Dois prazos."        →  problema em 2 palavras
③ "Uma bagunça."        →  consequência em 2 palavras (gradient chama atenção)
④ Badge "31/maio"       →  urgência — o elemento mais quente visualmente
⑤ Cards PF / PJ        →  detalhe — o viewer entende os dois mundos
⑥ Subtítulo + body      →  confirmação do que os cards mostram
⑦ Botão CTA             →  próximo passo
⑧ Logo rodapé           →  assinatura de autoridade
```

**Teste dos 2 segundos:** Badge + dois títulos + badge central = mensagem completa entendida antes do viewer processar os cards. ✅

---

## ━━━ ELEMENTOS TÉCNICOS DE GLASSMORPHISM ━━━

```
CARD PF (esquerdo)
├── background:    rgba(30, 41, 59, 0.75)
├── border:        1.5px solid rgba(14, 165, 233, 0.45)
├── backdrop-filter: blur(12px)
├