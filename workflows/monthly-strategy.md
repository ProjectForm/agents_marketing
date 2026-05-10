# Workflow: Estratégia Mensal

## Visão Geral
Executado no primeiro dia útil de cada mês. Analisa tendências, planeja campanhas especiais e define a estratégia de conteúdo do mês.

**Comando:** `python main.py --monthly`
**Quando executar:** Primeiro dia útil de cada mês

---

## Fluxo Completo

```
Primeiro dia útil do mês — 09:00

TrendAnalyzer
  ↓ Contexto sazonal do mês inteiro
  ↓ Datas fiscais e comemorativas
  ↓ Oportunidades temáticas

Content Strategist
  ↓ Análise de tendências do nicho
  ↓ Identificação de oportunidades únicas do mês
  ↓ Sugestões de campanhas especiais

Brand Director
  ↓ Planejamento mensal consolidado
  ↓ Campanhas especiais aprovadas
  ↓ Meta de output do mês
  ↓ Estratégia de crescimento

Output: output/calendarios/planejamento-YYYY-MM.md
```

---

## Calendário Anual de Campanhas Especiais

### Janeiro
- **MEI Anual:** Começa a comunicar (prazo até 31/maio)
- **Planejamento:** "Como organizar 2025 como MEI/freelancer"
- **Tom:** Renovação, novo começo, metas

### Fevereiro
- **Carnaval:** "As finanças não tiram férias" (empático, não negativo)
- **Preparação IRPF:** Primeiro aviso
- **Valentim:** Conteúdo sobre investir no negócio como amor próprio

### Março
- **IRPF COMEÇA** (campanha principal do mês)
- **Dia da Mulher (8/03):** MEIs e freelancers femininas em destaque
- **Tom:** Urgência suave, educacional forte

### Abril
- **IRPF em andamento** (campanha continuação)
- **Páscoa:** Relatable content sobre renda variável e "meses gordos/magros"
- **Tom:** Moderado, educacional

### Maio
- **IRPF último mês** (urgência aumenta nas últimas 2 semanas)
- **MEI Anual vence 31/maio** (campanha paralela)
- **Dia do Trabalho (01/05):** Homenagem ao trabalhador autônomo
- **Tom:** Urgência, celebração

### Junho
- **Balanço semestral:** "Você está no caminho certo?"
- **Alerta limite MEI:** Para quem está perto de R$ 81k
- **Festa Junina:** Conteúdo cultural leve + finanças
- **Tom:** Reflexivo, analítico

### Julho
- **Férias:** Empatia com freelancer que não tem férias pagas
- **Organização pré-Q4:** Preparação para segundas semestre
- **Tom:** Empático, motivacional

### Agosto
- **Agosto Dourado:** Bem-estar financeiro e saúde
- **Preparação para alta temporada** (se aplicável ao nicho)
- **Tom:** Equilibrado, bem-estar

### Setembro
- **Setembro Amarelo:** Saúde mental + pressão financeira do freelancer (cuidadoso)
- **Organização para Q4:** Urgência de planejamento
- **Tom:** Cuidadoso, empático, mas motivacional

### Outubro
- **Pré-Black Friday:** Como o MEI pode se preparar para vender mais
- **Revisão anual:** A 3 meses do ano acabar — check-in financeiro
- **Tom:** Estratégico, oportunidade

### Novembro
- **BLACK FRIDAY** (campanha principal)
  - Semana 1: "Como o MEI pode aproveitar a BF"
  - Semana 2-3: Promoção do Finlancer na BF (se houver)
  - Semana 4: Pós-BF, balanço
- **Tom:** Urgência, oportunidade

### Dezembro
- **Fechamento financeiro:** Balanço anual
- **13° MEI:** Como calcular pró-labore de fim de ano
- **Planejamento 2026:** Preparação para o novo ano
- **Natal/Réveillon:** Gratidão + conquistas do ano
- **Tom:** Reflexivo, celebração, esperança

---

## Estrutura do Planejamento Mensal

O arquivo `planejamento-YYYY-MM.md` contém:

```markdown
# Planejamento Mensal — [Mês Ano]

## Eventos Fiscais do Mês
- [Lista de datas e eventos relevantes]

## Campanhas Especiais
- [Campanhas ativas no mês]

## Pilares por Semana
- Semana 1: [Tema + pilar principal]
- Semana 2: [Tema + pilar principal]
- Semana 3: [Tema + pilar principal]
- Semana 4: [Tema + pilar principal]

## Meta de Output do Mês
- Instagram: X posts
- TikTok: X vídeos
- Facebook: X posts
- YouTube: X shorts

## Oportunidades Únicas do Mês
[O que só pode ser feito/dito neste mês]

## Estratégia de Crescimento
[Foco de crescimento: alcance, engajamento ou conversão]

## Ajustes vs. Mês Anterior
[O que mudar com base em desempenho]
```

---

## KPIs Mensais para Acompanhar

| Métrica | Meta | Período |
|---------|------|---------|
| Posts publicados | 80+ | Mês |
| Carrosséis produzidos | 12+ | Mês |
| Roteiros UGC | 20+ | Mês |
| Taxa de aprovação (1ª versão) | 85%+ | Mês |
| Diversidade de formatos | 4+ | Mês |
| Menção diferencial PF+PJ | 8+/mês | Mês |

---

## Uso

```bash
# Planejamento do mês atual
python main.py --monthly
```
