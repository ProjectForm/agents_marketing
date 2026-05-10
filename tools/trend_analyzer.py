import logging
from datetime import datetime

logger = logging.getLogger(__name__)


FISCAL_CALENDAR = {
    1:  ["MEI Anual começa (prazo até 31/maio)", "Planejamento financeiro do ano"],
    2:  ["Preparação IRPF", "Organização financeiro Q1"],
    3:  ["IRPF inicia", "Dia Internacional da Mulher (empreendedoras)"],
    4:  ["IRPF em andamento", "Prazo se aproximando"],
    5:  ["Último mês IRPF (prazo 31/maio)", "MEI Anual vence 31/maio"],
    6:  ["Metade do ano — balanço financeiro", "Alerta limite MEI R$81k"],
    7:  ["Férias escolares — freelancer não tira férias fácil", "Revisão contratos"],
    8:  ["Preparação para Q4", "Bem-estar financeiro"],
    9:  ["Setembro Amarelo + saúde mental freelancer", "Organização para Q4"],
    10: ["Pré-Black Friday para MEIs", "Revisão faturamento — limite MEI"],
    11: ["Black Friday", "Último DAS de folga antes do fechamento"],
    12: ["Fechamento financeiro do ano", "13° e pró-labore", "Planejamento 2025"],
}

NICHO_TRENDING_TOPICS = [
    "Como pagar menos imposto sendo MEI",
    "Separar conta PF de PJ",
    "Limite de faturamento MEI",
    "Contrato freelancer: como fazer",
    "DAS em atraso: o que fazer",
    "Precificação para freelancers",
    "Reserva de emergência renda variável",
    "IRPF MEI: o que declarar",
    "Nota fiscal autônomo: quando emitir",
    "Pró-labore: como se pagar sendo MEI",
    "Gastos que MEI pode deduzir",
    "Diferença MEI e ME",
    "Como abrir CNPJ sendo freelancer",
    "Organizar finanças do negócio sem contador",
]

EVERGREEN_CONTENT_IDEAS = [
    {
        "theme": "Separação PF vs PJ",
        "hook": "Você usa o mesmo cartão para tudo? Isso está custando mais caro do que você imagina.",
        "format": ["carrossel", "reel"],
        "pilar": "educacional",
    },
    {
        "theme": "DAS: tudo que você precisa saber",
        "hook": "Todo dia 20 aparece aquele boleto. Você sabe exatamente o que está pagando?",
        "format": ["carrossel", "reel_educacional"],
        "pilar": "educacional",
    },
    {
        "theme": "Erros comuns do MEI iniciante",
        "hook": "Fiz esses 3 erros no meu primeiro ano de MEI. Você pode evitar.",
        "format": ["reel_ugc", "carrossel"],
        "pilar": "educacional",
    },
    {
        "theme": "Pró-labore: como se pagar",
        "hook": "MEI que paga tudo da empresa e fica sem dinheiro pessoal — isso tem solução.",
        "format": ["reel", "facebook_post"],
        "pilar": "educacional",
    },
    {
        "theme": "Contrato freelancer",
        "hook": "Já trabalhou sem contrato e o cliente some? Nunca mais.",
        "format": ["reel_ugc", "carrossel"],
        "pilar": "educacional",
    },
]


class TrendAnalyzer:
    """Fornece contexto de tendências e sazonalidade para os agentes."""

    def get_seasonal_context(self, date: datetime = None) -> dict:
        date = date or datetime.now()
        month = date.month
        day = date.day

        context = {
            "month": month,
            "day": day,
            "month_events": FISCAL_CALENDAR.get(month, []),
            "das_alert": None,
            "urgent_topics": [],
        }

        # Alerta DAS: na semana anterior ao dia 20
        if 13 <= day <= 19:
            days_to_das = 20 - day
            context["das_alert"] = f"DAS vence em {days_to_das} dia(s)"
            context["urgent_topics"].append(f"DAS vence em {days_to_das} dias")

        # Alerta DAS: no próprio dia 20
        if day == 20:
            context["das_alert"] = "DAS vence HOJE"
            context["urgent_topics"].append("DAS vence hoje — urgência suave")

        # IRPF
        if month in [3, 4, 5]:
            context["urgent_topics"].append("Temporada IRPF em andamento")
            if month == 5:
                context["urgent_topics"].append("Último mês do IRPF — urgência aumenta")

        # MEI Anual
        if month == 1:
            context["urgent_topics"].append("MEI Anual: começa a pensar no prazo")
        if month == 4 or (month == 5 and day <= 25):
            context["urgent_topics"].append(f"MEI Anual vence em 31/maio — {'urgente' if month == 5 else 'prepare-se'}")

        # Black Friday
        if month == 11:
            context["urgent_topics"].append("Black Friday: oportunidade para MEIs")

        return context

    def get_content_suggestions(self, count: int = 5) -> list[dict]:
        import random
        all_ideas = EVERGREEN_CONTENT_IDEAS + [
            {"theme": topic, "hook": f"Tudo sobre: {topic}", "format": ["carrossel"], "pilar": "educacional"}
            for topic in NICHO_TRENDING_TOPICS
        ]
        return random.sample(all_ideas, min(count, len(all_ideas)))

    def get_weekly_brief_context(self, week_start: datetime = None) -> str:
        week_start = week_start or datetime.now()
        seasonal = self.get_seasonal_context(week_start)
        suggestions = self.get_content_suggestions(3)

        lines = [
            f"## Contexto da Semana — {week_start.strftime('%d/%m/%Y')}",
            "",
            "### Eventos Fiscais",
        ]
        for event in seasonal["month_events"]:
            lines.append(f"- {event}")

        if seasonal["das_alert"]:
            lines.append(f"\n⚠️ **ALERTA DAS:** {seasonal['das_alert']}")

        if seasonal["urgent_topics"]:
            lines.append("\n### Tópicos Urgentes")
            for t in seasonal["urgent_topics"]:
                lines.append(f"- {t}")

        lines.append("\n### Sugestões de Conteúdo")
        for s in suggestions:
            lines.append(f"- **{s['theme']}** — Gancho: _{s['hook']}_")

        return "\n".join(lines)
