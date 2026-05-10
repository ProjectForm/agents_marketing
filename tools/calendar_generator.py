import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

WEEKDAYS_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


class CalendarGenerator:
    """Gera e gerencia o calendário editorial do Finlancer."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path(__file__).parent.parent / "output"

    def get_week_dates(self, start_date: datetime = None) -> list[datetime]:
        start = start_date or datetime.now()
        # Começa na segunda-feira da semana
        monday = start - timedelta(days=start.weekday())
        return [monday + timedelta(days=i) for i in range(5)]  # Segunda a sexta

    def format_week_header(self, week_dates: list[datetime]) -> str:
        start = week_dates[0].strftime("%d/%m")
        end = week_dates[-1].strftime("%d/%m/%Y")
        return f"Semana {week_dates[0].strftime('%W')} | {start} a {end}"

    def generate_weekly_template(self, week_dates: list[datetime], theme: str = "") -> str:
        header = self.format_week_header(week_dates)
        lines = [
            f"# Calendário Editorial — {header}",
            f"\n## Tema da Semana",
            f"{theme or '[Definir após planning meeting]'}",
            "\n## Metas da Semana",
            "- Instagram: 15 posts (3/dia)",
            "- Reels roteiros: 5 (1 UGC por dia)",
            "- Carrosséis: 3",
            "- Facebook: 5",
            "- YouTube ideia: 1",
            "",
        ]

        for date in week_dates:
            weekday = WEEKDAYS_PT[date.weekday()]
            date_str = date.strftime("%d/%m")
            lines += [
                f"\n## {weekday} — {date_str}",
                "",
                "### Instagram",
                "- **Carrossel:** [Tema] | Pilar: [educacional/engajamento/promocional]",
                "  - Diferencial: [qual dos 5 diferenciais]",
                "  - Brief visual: [conceito]",
                "- **Reel 1:** [Tema] | [Formato]",
                "  - Gancho: [primeiros 3s]",
                "- **Reel 2 (UGC):** [Tema] | Persona: [tipo]",
                "  - Gancho: [primeiros 3s]",
                "- **Feed Estático:** [Tema]",
                "",
                "### TikTok",
                "- [Adaptação do Reel com tom mais casual]",
                "",
                "### Facebook",
                "- **Post storytelling:** [Tema]",
                "  - Estrutura: [situação→problema→solução→CTA]",
                "",
                "### Horários de Publicação Sugeridos",
                "- Instagram Reels: 19:00",
                "- Instagram Feed/Carrossel: 12:00",
                "- TikTok: 18:00",
                "- Facebook: 13:00",
                "",
                "---",
            ]

        return "\n".join(lines)

    def save_weekly_calendar(self, calendar_content: str, week_start: datetime = None) -> Path:
        week_start = week_start or datetime.now()
        monday = week_start - timedelta(days=week_start.weekday())
        filename = f"calendario-semana-{monday.strftime('%Y-%m-%d')}.md"

        output_path = self.output_dir / "calendarios"
        output_path.mkdir(parents=True, exist_ok=True)

        path = output_path / filename
        path.write_text(calendar_content, encoding="utf-8")
        logger.info(f"Calendário salvo: {path}")
        return path

    def get_next_das_date(self, from_date: datetime = None) -> datetime:
        today = from_date or datetime.now()
        if today.day < 20:
            return today.replace(day=20)
        # Próximo mês
        if today.month == 12:
            return today.replace(year=today.year + 1, month=1, day=20)
        return today.replace(month=today.month + 1, day=20)

    def days_until_das(self, from_date: datetime = None) -> int:
        today = from_date or datetime.now()
        next_das = self.get_next_das_date(today)
        return (next_das - today).days
