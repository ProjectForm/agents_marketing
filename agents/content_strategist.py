from .base_agent import BaseAgent


class ContentStrategist(BaseAgent):
    agent_key = "content_strategist"

    def create_weekly_calendar(self, week_start: str, trending_topics: list[str] = None) -> str:
        topics_str = ", ".join(trending_topics) if trending_topics else "pesquise tendências atuais"
        prompt = f"""Crie o calendário editorial completo para a semana iniciando em {week_start}.

Trending topics identificados: {topics_str}

Entregue:
1. Tema da semana (macro)
2. Calendário dia-a-dia (segunda a sexta) com:
   - Tema do dia + pilar de conteúdo
   - Formato por plataforma (Instagram carrossel, reels, feed; TikTok; Facebook)
   - Diferencial Finlancer a destacar
   - Gancho sugerido para os vídeos
3. Datas fiscais relevantes da semana
4. Relatório de tendências identificadas
5. Briefings resumidos para os outros agentes

Garanta variedade de formatos e temas únicos por dia."""
        return self.run(prompt, reset_history=True)

    def create_agent_briefing(self, agent_name: str, date_str: str, theme: str, details: str) -> str:
        prompt = f"""Crie o briefing específico para o {agent_name} para {date_str}.

Tema do dia: {theme}
Detalhes adicionais: {details}

O briefing deve incluir:
- Contexto completo do tema
- Demanda específica para este agente
- Tom e diretrizes
- Diferencial Finlancer a destacar
- Restrições específicas
- Referências de estilo ou tendências relevantes"""
        return self.run(prompt)

    def analyze_trends(self) -> str:
        prompt = """Analise as tendências atuais para o nicho MEI/freelancer/finanças no Brasil:

1. Trending topics nas redes sociais (Instagram, TikTok)
2. Datas fiscais relevantes nos próximos 30 dias
3. Formatos de conteúdo em alta no nicho
4. Oportunidades temáticas não exploradas
5. Sugestões de campanhas especiais para o período

Base sua análise no conhecimento do nicho e no calendário fiscal brasileiro."""
        return self.run(prompt, reset_history=True)
