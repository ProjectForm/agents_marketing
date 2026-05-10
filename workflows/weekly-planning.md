# Workflow: Planejamento Semanal

## Visão Geral
Executado toda segunda-feira de manhã. Gera o calendário editorial da semana, a paleta visual e o cronograma de publicação com os melhores horários para máximo engajamento.

**Comando:** `python main.py --weekly`
**Quando executar:** Toda segunda-feira

---

## Fluxo Completo

```
Segunda 08:00

TrendAnalyzer
  ↓ Contexto sazonal da semana
  ↓ Alertas: DAS, IRPF, datas fiscais
  ↓ Sugestões de trending topics

Content Strategist
  ↓ Calendário editorial completo (segunda a sexta)
  ↓ Temas diários + pilares de conteúdo
  ↓ Briefings para os agentes

Visual Content Creator (paralelo)
  ↓ Paleta visual da semana
  ↓ Diretrizes estéticas para consistência

Brand Director
  ↓ Validação do calendário
  ↓ Cronograma de publicação (horários por plataforma)
  ↓ Visão de máximo engajamento

CalendarGenerator
  ↓ Salvar em output/calendarios/
```

---

## Outputs do Planejamento Semanal

```
output/
└── calendarios/
    ├── calendario-semana-2025-05-05.md     ← Calendário editorial completo
    └── planejamento-2025-05.md             ← Planejamento mensal (se executado)
```

### Conteúdo do Calendário Semanal

O arquivo gerado contém:

1. **Tema da Semana** (macro)
2. **Calendário Dia-a-Dia** (segunda a sexta)
   - Tema do dia + pilar de conteúdo
   - Formato por plataforma
   - Diferencial Finlancer a destacar
   - Gancho sugerido para vídeos
   - Briefing para cada agente
3. **Datas Fiscais da Semana**
4. **Paleta Visual** com hex codes
5. **Cronograma de Publicação** por horário
6. **Meta de Engajamento** estimada

---

## Cronograma de Publicação — Melhores Horários

O Brand Director gera o cronograma otimizado. Referência base:

### Instagram @finlancer.app
| Formato | Horário | Dias | Justificativa |
|---------|---------|------|---------------|
| Reels | 19:00 | Seg-Sex | Pico de engajamento pós-trabalho |
| Carrossel | 12:00 | Seg, Qua, Sex | Almoço — público mais reflexivo |
| Feed Estático | 12:00 | Ter, Qui | Almoço alternado |
| Stories | 09:00 | Diário | Manhã de trabalho |

### TikTok @finlancerl
| Formato | Horário | Dias |
|---------|---------|------|
| Vídeo | 18:00 | Ter, Qui, Sáb |
| Vídeo | 21:00 | Seg, Qua |

### Facebook
| Formato | Horário | Dias |
|---------|---------|------|
| Post longo | 13:00 | Seg, Qua, Sex |
| Vídeo UGC | 11:00 | Ter, Qui |

### YouTube Shorts
| Formato | Horário | Dias |
|---------|---------|------|
| Short | 10:00 | Ter, Sex |

---

## Visão Consolidada da Semana

### Meta de Conteúdo
| Plataforma | Quantidade | Formatos |
|-----------|-----------|---------|
| Instagram | 15 posts | 3 carrosséis + 5 reels + 5 feeds + 5 stories |
| TikTok | 5 vídeos | UGC + educacional alternados |
| Facebook | 5 posts | Storytelling + vídeo UGC |
| YouTube | 1 short | Adaptação do melhor reel da semana |

### Sequência Estratégica de Alto Engajamento
A sequência ideal por semana (sugestão):

```
Segunda:   Carrossel educacional (gera saves) + Reel de impacto
Terça:     Post feed + UGC (melhor dia para UGC na maioria dos nichos)
Quarta:    Carrossel engajamento + Reel educacional
Quinta:    Post feed + UGC (segundo melhor dia para UGC)
Sexta:     Carrossel + Reel promocional leve (fim de semana lembrete)
```

---

## Integração com Google Agenda (Futuro)

Para adicionar eventos ao Google Agenda programaticamente, usar a Google Calendar API:

```python
# tools/google_calendar.py (a implementar)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def add_posting_event(date, time, platform, content_type, title):
    """Adiciona evento de publicação no Google Agenda."""
    # Implementar com OAuth2
    pass
```

Por enquanto: copiar o cronograma gerado manualmente para o Google Agenda ou Reportei.

---

## Uso

```bash
# Planejamento da semana atual
python main.py --weekly

# Planejamento a partir de data específica
python main.py --weekly --date 2025-05-05
```
