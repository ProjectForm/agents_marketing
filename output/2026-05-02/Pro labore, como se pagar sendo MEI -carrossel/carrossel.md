<!-- Aprovado pelo Brand Director em 2026-05-02 -->

## CARROSSEL

# CONCEITO VISUAL COMPLETO — CARROSSEL "PRÓ-LABORE: COMO SE PAGAR SENDO MEI"

**Formato:** 1080×1350px (4:5) | 8 slides | Dark Mode Obrigatório

---

## PALETA DA PEÇA

```
BACKGROUNDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Canvas principal    #0f172a   ████████
Card/Surface        #1e293b   ████████
Card elevado        #334155   ████████

ACCENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Emerald primary     #10b981   ████████
Emerald dark        #059669   ████████
Emerald light       #34d399   ████████
Sky blue            #0ea5e9   ████████
Gradiente           #10b981 → #0ea5e9

TEXTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Texto primário      #f1f5f9   ████████
Texto secundário    #94a3b8   ████████
Texto em emerald    #10b981   ████████

GLASSMORPHISM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Card fill           rgba(30,41,59,0.7)
Borda sutil         rgba(255,255,255,0.08)
Glow emerald        rgba(16,185,129,0.15)
```

---

## SISTEMA TIPOGRÁFICO

```
Inter ExtraBold 800  →  Títulos de capa e destaque (48-64px)
Inter Bold 700       →  Títulos de seção (32-40px)
Inter SemiBold 600   →  Labels, subtítulos (18-24px)
Inter Regular 400    →  Corpo de texto (16-18px)
Inter ExtraBold 800  →  Números/dados grandes (72-96px)

Line-height títulos: 1.1
Line-height corpo:   1.6
Letter-spacing labels: +0.08em (uppercase)
```

---

## ELEMENTOS VISUAIS RECORRENTES (SISTEMA)

```
CARD GLASSMORPHISM PADRÃO
┌─────────────────────────────────┐
│  Fill: rgba(30,41,59,0.7)       │
│  Border: 1px rgba(255,255,255,  │
│          0.08)                  │
│  Border-radius: 16px            │
│  Backdrop-blur: 12px            │
│  Box-shadow: 0 4px 32px         │
│    rgba(16,185,129,0.08)        │
└─────────────────────────────────┘

PÍLULA / TAG
┌──────────────┐
│  bg: #10b981 │  border-radius: 999px
│  text: #fff  │  padding: 6px 16px
│  Inter 600   │  font-size: 13px uppercase
└──────────────┘

DIVISOR EMERALD
━━━━━━━━━━━  width: 48px, height: 3px
cor: linear-gradient(90°, #10b981, #0ea5e9)
border-radius: 2px

NÚMERO GRANDE (slides de dado)
Font: Inter ExtraBold 800
Tamanho: 80-96px
Cor: gradiente #10b981 → #0ea5e9
Aplicar: -webkit-background-clip: text

ÍCONE CÍRCULO ACCENT
Círculo: 56×56px, bg rgba(16,185,129,0.15)
Borda: 1px solid rgba(16,185,129,0.3)
Ícone interno: 28px, cor #10b981
```

---

## WIREFRAMES SLIDE A SLIDE

---

### SLIDE 1 — CAPA (Hook Visual)

```
┌──────────────────────────────────────────┐  1080×1350px
│                                          │
│  [FUNDO #0f172a]                         │
│                                          │
│  ┌ GLOW RADIAL ────────────────────────┐ │
│  │  Centro: 540,500 | Raio: 380px      │ │
│  │  rgba(16,185,129,0.12) → transparent │ │
│  └────────────────────────────────────┘ │
│                                          │
│                                          │
│   [TOP — 120px do topo]                  │
│   ┌──────────────────────────────────┐   │
│   │  PÍLULA TAG                      │   │
│   │  "GUIA DO MEI"  bg:#10b981       │   │
│   │  Inter SemiBold 13px uppercase   │   │
│   │  centralizado, width: auto       │   │
│   └──────────────────────────────────┘   │
│                                          │
│   [ELEMENTO CENTRAL — y:280px]           │
│   ┌──────────────────────────────────┐   │
│   │  CARD GLASSMORPHISM 920×320px    │   │
│   │  Dois sub-cards lado a lado:     │   │
│   │                                  │   │
│   │  ┌──────────┐  ┌──────────┐      │   │
│   │  │  💼 PJ   │  │  👤 PF   │      │   │
│   │  │ R$8.200  │  │  R$ ???  │      │   │
│   │  │ faturado │  │  recebido│      │   │
│   │  │ #1e293b  │  │ #1e293b  │      │   │
│   │  └──────────┘  └──────────┘      │   │
│   │                                  │   │
│   │  Seta dupla ↔ entre os cards     │   │
│   │  cor: #10b981                    │   │
│   └──────────────────────────────────┘   │
│                                          │
│   [BLOCO TÍTULO — y:680px]               │
│   ┌──────────────────────────────────┐   │
│   │  DIVISOR EMERALD (centralizado)  │   │
│   │                                  │   │
│   │  "Seu negócio fatura."           │   │
│   │  Inter ExtraBold 52px #f1f5f9    │   │
│   │  line-height: 1.1                │   │
│   │                                  │   │
│   │  "Mas quanto VOCÊ                │   │
│   │   está recebendo?"               │   │
│   │  Inter ExtraBold 52px            │   │
│   │  "VOCÊ" em gradiente emerald→sky │   │
│   │                                  │   │
│   │  Subtítulo 20px Inter Regular    │   │
│   │  #94a3b8                         │   │
│   │  "O guia completo do pró-labore  │   │
│   │   para MEI"                      │   │
│   └──────────────────────────────────┘   │
│                                          │
│   [RODAPÉ — y:1260px]                    │
│   Logo Finlancer  |  @finlancer.app      │
│   #94a3b8, Inter Regular 14px            │
│                                          │
└──────────────────────────────────────────┘

ELEMENTO DECORATIVO:
— Círculo grande translúcido no canto sup. direito
  400×400px, rgba(16,185,129,0.04)
  border: 1px solid rgba(16,185,129,0.08)
  overflow: hidden (cortado pela borda)
— Círculo menor no canto inf. esq.
  200×200px, mesma especificação
```

---

### SLIDE 2 — O PROBLEMA

```
┌──────────────────────────────────────────┐
│  [FUNDO #0f172a]                         │
│                                          │
│  [TOPO — y:80px, centralizado]           │
│   PÍLULA TAG: "O PROBLEMA"               │
│   bg: rgba(16,185,129,0.15)              │
│   border: 1px solid rgba(16,185,129,0.3) │
│   text: #10b981                          │
│                                          │
│  [TÍTULO — y:150px]                      │
│   "Quando você não define               │
│    quanto se pagar..."                   │
│   Inter Bold 38px #f1f5f9               │
│   text-align: left, margin: 0 80px      │
│   DIVISOR EMERALD (esq, y:240px)        │
│                                          │
│  [LISTA DE PROBLEMAS — y:280px]          │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │  CARD GLASSMORPHISM  920×140px   │    │
│  │  ⚠ ícone 28px #10b981            │    │
│  │  "O dinheiro que entra no CNPJ  │    │
│  │   parece

---

## FEED

# CONCEITO VISUAL — POST DE FEED ESTÁTICO
**"Pró-labore: como se pagar sendo MEI"**
**Formato:** 1080×1080px (1:1) | Dark Mode | Feed Instagram @finlancer.app

---

## DECISÃO DE FORMATO

```
Escolha: 1080×1080px (1:1)

Justificativa: Post estático de impacto único —
objetivo é parar o scroll com uma pergunta visual
poderosa. O quadrado perfeito funciona melhor para
composição simétrica com dois cards PF×PJ lado a
lado, que é o visual central desta peça.
O 4:5 fica reservado para o carrossel do mesmo tema.
```

---

## CONCEITO CRIATIVO

```
IDEIA CENTRAL:
"A dúvida que todo MEI tem, visualizada"

O post mostra dois cards lado a lado:
— Card ESQUERDO (🏢 PJ):  número concreto, cor sólida
— Card DIREITO  (👤 PF):  número com "???" ou vazio,
                           criando tensão visual

A assimetria de informação É a mensagem.
O viewer entende o problema em 2 segundos
sem precisar ler uma palavra.

HIERARQUIA DE LEITURA (sequência natural do olho):
1. Os dois cards contrastantes (visual)
2. A pergunta principal centralizada abaixo
3. O subtítulo explicativo
4. Tag/pílula de contexto (IRPF)
5. Logo Finlancer no rodapé
```

---

## WIREFRAME DETALHADO

```
┌─────────────────────────────────────────────┐
│              1080 × 1080 px                 │
│                                             │
│  [FUNDO BASE: #0f172a]                      │
│                                             │
│  [GLOW RADIAL — centro 540,480]             │
│   Raio: 420px                               │
│   rgba(16,185,129,0.10) → transparent       │
│   Posição: centro-alto                      │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │  PÍLULA CONTEXTUAL — y:72px           │  │
│  │  centralizada                         │  │
│  │  "IRPF FECHA EM 29 DIAS"             │  │
│  │  bg: rgba(16,185,129,0.12)           │  │
│  │  border: 1px solid rgba(16,185,      │  │
│  │          129,0.35)                   │  │
│  │  text: #10b981                       │  │
│  │  Inter SemiBold 600, 13px            │  │
│  │  uppercase, letter-spacing: 0.1em    │  │
│  │  border-radius: 999px                │  │
│  │  padding: 8px 20px                   │  │
│  └───────────────────────────────────────┘  │
│                                             │
│                                             │
│  [BLOCO DOIS CARDS — y:160px]               │
│   Dois cards lado a lado, gap: 24px         │
│   Cada card: 460×280px                      │
│   Margem lateral: 80px                      │
│                                             │
│  ┌────────────────┐   ┌────────────────┐    │
│  │  CARD PJ  🏢   │   │  CARD PF  👤   │    │
│  │                │   │                │    │
│  │ bg:#1e293b     │   │ bg:#1e293b     │    │
│  │ border:1px     │   │ border:1px     │    │
│  │ rgba(16,185,   │   │ rgba(255,255,  │    │
│  │ 129,0.25)      │   │ 255,0.06)      │    │
│  │ (borda emerald │   │ (borda neutra  │    │
│  │ sutil — ativo) │   │ — "vazio")     │    │
│  │ radius: 16px   │   │ radius: 16px   │    │
│  │                │   │                │    │
│  │ Label topo:    │   │ Label topo:    │    │
│  │ "SEU NEGÓCIO"  │   │ "VOCÊ"         │    │
│  │ #94a3b8        │   │ #94a3b8        │    │
│  │ Inter 600 12px │   │ Inter 600 12px │    │
│  │ uppercase      │   │ uppercase      │    │
│  │                │   │                │    │
│  │ Valor:         │   │ Valor:         │    │
│  │ "R$ 8.200"     │   │  "R$ ???"      │    │
│  │ Inter ExBold   │   │  Inter ExBold  │    │
│  │ 800, 48px      │   │  800, 48px     │    │
│  │ #f1f5f9        │   │  #94a3b8 +     │    │
│  │                │   │  opacity:0.5   │    │
│  │ Sub-label:     │   │                │    │
│  │ "faturado/mês" │   │ Sub-label:     │    │
│  │ #94a3b8 14px   │   │ "recebido/mês" │    │
│  │                │   │ #94a3b8 14px   │    │
│  │ [DOT verde     │   │ [DOT cinza     │    │
│  │  8×8px         │   │  8×8px         │    │
│  │  #10b981]      │   │  #475569]      │    │
│  └────────────────┘   └────────────────┘    │
│                                             │
│  [SETA BIDIRECIONAL entre os cards]         │
│   Position: absoluta, centro entre cards    │
│   y: 300px (centro vertical dos cards)     │
│   ↔  símbolo 32px, cor: #10b981            │
│   bg: #0f172a, padding: 4px                │
│   (cria "corte" na linha divisória)        │
│                                             │
│                                             │
│  [DIVISOR EMERALD — y:470px]                │
│   width: 48px, height: 3px                 │
│   linear-gradient(90°,#10b981,#0ea5e9)     │
│   centralizado                              │
│                                             │
│                                             │
│  [BLOCO TÍTULO — y:496px]                   │
│                                             │
│   LINHA 1 — Pergunta principal:             │
│   "Quanto você se paga"                     │
│   Inter ExtraBold 800, 52px                 │
│   #f1f5f9, text-align: center               │
│   line-height: 1.1                          │
│                                             │
│   LINHA 2 — com destaque:                   │
│   "do seu próprio negócio?"                 │
│   Inter ExtraBold 800, 52px                 │
│   "próprio negócio" em gradiente:           │
│   linear-gradient(90°,#10b981,#0ea5e9)     │
│   text-align: center                        │
│                                             │
│                                             │
│  [SUBTÍTULO — y:640px]                      │
│   "Pró-labore é o salário que você          │
│    define pagar a si mesmo como MEI."       │
│   Inter Regular 400, 18px                   │
│   #94a3b8, text-align: center               │
│   max-width: 760px, centralizado            │
│   line-height: 1.6                          │
│                                             │
│                                             │
│  [RODAPÉ — y:980px]                         │
│   Layout: flex, space-between               │
│   margin: 0 80px                            │
│                                             │
│   ESQUERDA:                                 │
│   Logotipo Finlancer                        │
│   Inter ExtraBold 800, 20px                 │
│   "Finlancer" — "F" em #10b981,             │
│   restante em #f1f5f9                        │
│                                             │
│   DIREITA:                                  │
│   "@finlancer.app"                          │
│   Inter Regular 400, 15px                   │
│   #94a3b8                                   │
│                                             │
│   LINHA DIVISÓRIA ACIMA DO RODAPÉ:          │
│   1px solid rgba(255,255,255,0.06)          │
│   width: 920px, centralizada                │
│   y: 965px                                  │
│                                             │
└─────────────────────────────────────────────┘

ELEMENTOS DECORATIVOS (z-index baixo):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
— Círculo grande sup. direito:
  360×360px, rgba(16,185,129,0.04)
  border: 1px solid rgba(16,185,129,0.07)
  overflow