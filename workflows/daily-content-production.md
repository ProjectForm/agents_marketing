# Workflow: Produção Diária de Conteúdo

## Visão Geral
Rotina automatizada que gera diariamente o pacote completo de conteúdo para todas as plataformas do Finlancer.

**Comando:** `python main.py`
**Duração estimada:** 15-25 minutos (dependência da API)

---

## Fluxo Completo

```
08:00  Brand Director + Content Strategist
         ↓ Planning Meeting
         ↓ Briefing do dia

09:00  ┌─ Social Copy Specialist ─────────────┐
       │  4 legendas IG + 1 FB + 1 TikTok     │
       │                                        │  (paralelo)
       ├─ Visual Content Creator ───────────────┤
       │  1 carrossel + 1 feed + prompts AI     │
       │                                        │
       └─ Video Script Specialist ──────────────┘
          2 roteiros (1 Reel + 1 UGC obrigatório)

11:00  Content Strategist
         ↓ Revisão de coerência entre os outputs

12:00  Brand Director
         ↓ Aprovação final ou solicitação de ajustes

12:30  OutputManager
         ↓ Salvar arquivos organizados por plataforma
         ↓ Gerar INDEX.md da pasta do dia
```

---

## Outputs Gerados

### Pasta: `output/YYYY-MM-DD/`

```
output/
└── 2025-05-01/
    ├── INDEX.md                      ← Índice de todos os arquivos
    ├── instagram/
    │   ├── legendas.md               ← 4 legendas (reels, carrossel, feed)
    │   ├── carrossel-conceito.md     ← Wireframe + paleta + prompts Canva
    │   ├── reels-roteiros.md         ← Roteiro do Reel não-UGC
    │   └── visual-conceito.md        ← Conceito visual completo
    ├── facebook/
    │   └── post-storytelling.md      ← Post longo estilo blog
    ├── tiktok/
    │   └── roteiro-video.md          ← Roteiro UGC + briefing creator
    └── youtube/
        └── ideia-video.md            ← Ideia adaptada para Shorts
```

---

## Checklist de Qualidade (Brand Director verifica)

### Copy
- [ ] Segunda pessoa ("você") em todos os textos
- [ ] CTA presente em cada peça
- [ ] Sem anglicismos desnecessários
- [ ] Tom adequado à plataforma
- [ ] Diferencial PF+PJ mencionado (ao menos 1 peça)
- [ ] Nenhuma promessa de enriquecimento

### Visual
- [ ] Dark mode (#0f172a background)
- [ ] Emerald #10b981 como cor principal
- [ ] Texto fora da zona de risco (20% inferior) nos Reels
- [ ] Hierarquia visual clara em cada slide
- [ ] Prompts AI prontos para execução no Canva

### Vídeo
- [ ] Gancho nos primeiros 3 segundos
- [ ] 1 dos 2 roteiros é UGC
- [ ] Briefing de produção completo
- [ ] Duração dentro do limite (15-60s)
- [ ] Sugestão de trilha sonora incluída

---

## Uso com Tema Customizado

```bash
# Produção normal
python main.py

# Tema específico
python main.py --custom "erros comuns do MEI no primeiro ano"

# Data específica
python main.py --date 2025-05-20

# Tema + data
python main.py --date 2025-05-20 --custom "DAS vence hoje — o que fazer"
```

---

## Integração com Reportei (Agendamento Manual)

Após a produção, o conteúdo fica pronto em `output/YYYY-MM-DD/`.

Sequência recomendada para agendamento no Reportei:

| Horário | Plataforma | Tipo | Arquivo |
|---------|-----------|------|---------|
| 12:00 | Instagram | Carrossel | `instagram/legendas.md` + conceito visual |
| 19:00 | Instagram | Reel | `instagram/reels-roteiros.md` |
| 13:00 | Facebook | Post | `facebook/post-storytelling.md` |
| 18:00 | TikTok | Vídeo | `tiktok/roteiro-video.md` |
| 10:00* | Instagram | Feed | `instagram/legendas.md` (legenda feed) |

*Quando for dia de post de feed estático

---

## Resolução de Problemas

### Agente retornou output insatisfatório
O Brand Director sinaliza com "REVISAR" ou "BLOQUEADO".
Re-execute apenas o agente específico:

```python
from anthropic import Anthropic
from agents import SocialCopySpecialist

client = Anthropic()
copy = SocialCopySpecialist(client)
result = copy.create_full_copy_package(
    theme="seu tema aqui",
    briefing="briefing específico aqui"
)
print(result)
```

### Erro de API
Verifique `logs/agency-YYYY-MM-DD.log` para detalhes.
O sistema tem retry automático: 3 tentativas com backoff exponencial.
