<!-- Aprovado pelo Brand Director em 2026-05-01 -->

## CARROSSEL

# CONCEITO VISUAL COMPLETO — CARROSSEL 8 SLIDES
## "Os erros que todo MEI comete no primeiro ano"
### Finlancer | 01/05/2026 | Dia do Trabalhador

---

## 1. PALETA DA PEÇA

```
CORES PRIMÁRIAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Background principal    #0f172a   ████
Surface (cards)         #1e293b   ████
Surface elevado         #334155   ████

CORES DE DESTAQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Emerald (primária)      #10b981   ████
Emerald escuro          #059669   ████
Emerald claro           #34d399   ████
Gradiente               #10b981 → #0ea5e9

TEXTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Texto primário          #f1f5f9   ████
Texto secundário        #94a3b8   ████
Texto desativado        #475569   ████

ACENTO / URGÊNCIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Amber (alerta suave)    #f59e0b   ████
Amber escuro            #d97706   ████

BORDA GLASS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rgba(255,255,255,0.08)  — bordas cards
rgba(16,185,129,0.20)   — bordas com destaque emerald
```

---

## 2. SISTEMA TIPOGRÁFICO DA PEÇA

```
HIERARQUIA TIPOGRÁFICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
T1 — Título Principal    Inter ExtraBold 800   52-60px
T2 — Título de Erro      Inter Bold 700        38-44px
T3 — Número do Erro      Inter ExtraBold 800   80-96px
T4 — Corpo               Inter Regular 400     20-22px
T5 — Subtítulo/Label     Inter SemiBold 600    18-20px
T6 — Caption/Rodapé      Inter Medium 500      14-16px
T7 — Badge/Tag           Inter Bold 700        13-15px
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Line-height padrão: 1.4 para títulos | 1.6 para corpo
Letter-spacing títulos: -0.02em
```

---

## 3. COMPONENTES REUTILIZÁVEIS (Sistema de Design)

```
┌─────────────────────────────────────────────────┐
│  CARD GLASS — componente base de todos os slides│
│                                                 │
│  Background:  #1e293b                           │
│  Border:      1px solid rgba(255,255,255,0.08)  │
│  Border-rad:  20px                              │
│  Backdrop:    blur(12px)                        │
│  Padding:     48px                              │
│  Shadow:      0 8px 32px rgba(0,0,0,0.40)       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  BADGE DE URGÊNCIA                              │
│                                                 │
│  Background:  rgba(16,185,129,0.15)             │
│  Border:      1px solid rgba(16,185,129,0.40)   │
│  Border-rad:  100px (pill)                      │
│  Text:        #10b981, Inter Bold, 13px         │
│  Padding:     6px 14px                          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  NÚMERO DO ERRO (elemento decorativo grande)    │
│                                                 │
│  Cor:         rgba(16,185,129,0.12)             │
│  Font:        Inter ExtraBold 800               │
│  Size:        200-240px (elemento de fundo)     │
│  Position:    canto superior direito, cortado   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  LINHA DIVISÓRIA EMERALD                        │
│                                                 │
│  Width:       48px                              │
│  Height:      3px                               │
│  Background:  gradiente #10b981 → #0ea5e9       │
│  Border-rad:  2px                               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  RODAPÉ PADRÃO (todos os slides)                │
│                                                 │
│  Logo Finlancer — esquerda                      │
│  "finlancer.com.br" — direita                   │
│  Cor: #475569                                   │
│  Separador: linha 1px rgba(255,255,255,0.06)    │
│  Altura: 56px                                   │
└─────────────────────────────────────────────────┘
```

---

## 4. WIREFRAMES SLIDE-A-SLIDE

---

### SLIDE 1 — CAPA
**Dimensão:** 1080 × 1350px

```
┌──────────────────────────────────────────────┐ ← #0f172a
│                                              │
│  ┌─ BADGE URGÊNCIA ─────────────────────┐   │ ← y: 64px
│  │  🗓  Prazo: 31 de maio               │   │   emerald pill
│  └──────────────────────────────────────┘   │
│                                              │
│                                              │
│  ░░░░░░░░░░ [ELEMENTO GRÁFICO] ░░░░░░░░░░   │
│                                              │
│     ┌────────────────────────────────────┐   │
│     │                                    │   │
│     │  Fundo: padrão de pontos           │   │ ← grid dots
│     │  rgba(16,185,129,0.06)             │   │   72px gap
│     │                                    │   │
│     │  [ÍCONE CENTRAL]                   │   │ ← 96x96px
│     │  ⚠  ícone triângulo alerta         │   │   #10b981
│     │  stroke, outline style             │   │   y: centro-100px
│     │                                    │   │
│     └────────────────────────────────────┘   │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │                                        │  │ ← card glass
│  │  5 ERROS QUE TODO MEI            52px  │  │   padding: 48px
│  │  COMETE NO                             │  │   Inter ExtraBold
│  │  PRIMEIRO ANO                          │  │   #f1f5f9
│  │                                        │  │
│  │  ══════════════                        │  │ ← linha 48px emerald
│  │                                        │  │
│  │  E que cobram o preço          20px    │  │   Inter Regular
│  │  justamente agora — em maio.           │  │   #94a3b8
│  │                                        │  │
│  │  ┌──────────────────────────────────┐  │  │
│  │  │  Deslize para não repetir  →     │  │  │ ← micro CTA
│  │  └──────────────────────────────────┘  │  │   rgba glass pill
│  │                                        │  │   #94a3b8 14px
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ finlancer          finlancer.com.br      ││ ← rodapé padrão
│  └──────────────────────────────────────────┘│
└──────────────────────────────────────────────┘

ESPECIFICAÇÕES ADICIONAIS:
• Gradiente de fundo sutil: radial em #10b981 opacity 4%,
  centralizado no ícone — cria aura de luz suave
• Ícone: outline, stroke 2px, cor #10b981
• Número "5" em #10b981 atrás do ícone, 240px, opacity 8%
• Badge: canto superior esquerdo, x:64px y:64px
```

---

### SLIDE 2 —

---

## FEED

# CONCEITO VISUAL — POST DE FEED ESTÁTICO
## "Erros do MEI no Primeiro Ano" | Dia do Trabalhador
### Finlancer | 01/05/2026

---

## DECISÃO DE FORMATO

```
FORMATO ESCOLHIDO: 1080 × 1350px (4:5)
JUSTIFICATIVA:
  → Ocupa mais espaço no feed — maior impacto visual
  → Permite acomodar os 5 erros em lista vertical com respiro
  → Melhor hierarquia para o volume de informação necessário
  → Performa melhor que 1:1 em alcance orgânico no Instagram
```

---

## 1. CONCEITO CRIATIVO

```
CONCEITO: "A Lista que Todo MEI Precisava Ver"

LÓGICA VISUAL:
  Inspiração em dashboards financeiros — o post parece
  uma tela do próprio Finlancer. Cada erro aparece como
  um "item de auditoria" marcado com ícone de alerta,
  reforçando que o app detectaria esses problemas
  automaticamente.

TENSÃO VISUAL:
  Contraste entre os 5 erros em vermelho/amber suave
  e a solução em emerald — a narrativa "problema → saída"
  acontece dentro de um único post.

ÂNCORA DE DATA:
  Badge "1º de Maio — Dia do Trabalhador" integrado ao
  design sem dominar — é reconhecimento, não celebração.
```

---

## 2. PALETA DA PEÇA

```
CORES DESTA PEÇA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Background          #0f172a    ████  fundo principal
Surface card        #1e293b    ████  card central
Surface elevado     #243044    ████  linhas de erro (hover)
Borda glass         rgba(255,255,255,0.07)   bordas suaves
Borda glass forte   rgba(255,255,255,0.12)   borda card principal

DESTAQUE E MARCA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Emerald             #10b981    ████  CTA, ícone solução, logo
Emerald glow        rgba(16,185,129,0.12)    aura de fundo
Gradiente           #10b981 → #0ea5e9        elemento decorativo

ALERTA (erros)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Amber               #f59e0b    ████  ícone de alerta dos erros
Amber bg            rgba(245,158,11,0.08)    fundo linha de erro
Amber borda         rgba(245,158,11,0.20)    borda linha de erro

TEXTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primário            #f1f5f9    ████  títulos, itens principais
Secundário          #94a3b8    ████  subtítulos, descrições
Terciário           #475569    ████  rodapé, labels
```

---

## 3. SISTEMA TIPOGRÁFICO

```
HIERARQUIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
T1 Título principal    Inter ExtraBold 800   52px
T2 Subtítulo           Inter Regular 400     20px
T3 Label de seção      Inter SemiBold 600    13px  uppercase
T4 Texto dos erros     Inter SemiBold 600    22px
T5 Descrição           Inter Regular 400     17px
T6 Rodapé / CTA tag    Inter Medium 500      14px
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Line-height T1: 1.15
Line-height T4: 1.3
Line-height T5: 1.5
Letter-spacing T3 (label): 0.08em
```

---

## 4. WIREFRAME DETALHADO

```
┌────────────────────────────────────────────┐
│                 1080 × 1350px              │
│                  #0f172a                   │
│                                            │
│  · · · · · · · · · · · · · · · · · · · ·  │ ← grid de pontos
│  · · · · · · · · · · · · · · · · · · · ·  │   rgba(255,255,255
│  · · · · · · · · · · · · · · · · · · · ·  │   ,0.03) 40px gap
│                                            │
│  ┌──────────────────────────────────────┐  │ ← x:48 y:56
│  │  ZONA A — HEADER                     │  │   width: 984px
│  │                                      │  │
│  │  [BADGE ESQUERDA]   [BADGE DIREITA]  │  │
│  │  ● 1º de Maio       🗓 Prazo: 31/mai │  │ ← duas pills
│  │  Dia do Trabalhador                  │  │   altura: 32px
│  │                                      │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │ ← card principal
│  │  #1e293b | border-radius: 24px       │  │   x:48 y:130
│  │  border: rgba(255,255,255,0.10)      │  │   width: 984px
│  │  padding: 48px                       │  │   height: 1108px
│  │                                      │  │
│  │  ┌────────────────────────────────┐  │  │
│  │  │  ZONA B — TÍTULO               │  │  │ ← y interno: 48px
│  │  │                                │  │  │
│  │  │  ⚠  [LABEL UPPERCASE]          │  │  │ ← ícone 20px amber
│  │  │  ERROS DO MEI  13px #94a3b8    │  │  │   letter-spacing
│  │  │                                │  │  │
│  │  │  5 erros que          52px     │  │  │ ← Inter ExtraBold
│  │  │  todo MEI comete      #f1f5f9  │  │  │   line-height 1.15
│  │  │  no primeiro ano               │  │  │
│  │  │                                │  │  │
│  │  │  ████████████████              │  │  │ ← linha gradiente
│  │  │  48px × 3px emerald→sky        │  │  │   margin-top: 16px
│  │  │                                │  │  │
│  │  │  e que cobram o preço  20px    │  │  │ ← Inter Regular
│  │  │  justamente agora.     #94a3b8 │  │  │   margin-top: 20px
│  │  └────────────────────────────────┘  │  │
│  │                                      │  │
│  │  ══════════════════════════════════  │  │ ← divisória
│  │  1px rgba(255,255,255,0.06)          │  │   margin: 32px 0
│  │                                      │  │
│  │  ┌────────────────────────────────┐  │  │ ← ZONA C — LISTA
│  │  │  LINHA ERRO 01                 │  │  │
│  │  │  ┌──────────────────────────┐  │  │  │ ← item glass
│  │  │  │ bg: rgba(245,158,11,0.06)│  │  │  │   border-radius:12px
│  │  │  │ border: rgba(245,158,11  │  │  │  │   border amber 0.15
│  │  │  │         ,0.18) 1px       │  │  │  │   padding: 16px 20px
│  │  │  │ height: 68px             │  │  │  │
│  │  │  │                          │  │  │  │
│  │  │  │ ⚠  Misturar PF e PJ  22px│  │  │  │ ← amber ⚠ 20px
│  │  │  │    Cartão pessoal p/     │  │  │  │   Inter SemiBold
│  │  │  │    despesas do negócio   │  │  │  │   texto #f1f5f9
│  │  │  └──────────────────────────┘  