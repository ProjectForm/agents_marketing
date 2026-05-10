import os
import time
import logging
import yaml
from pathlib import Path
from anthropic import Anthropic

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent.parent / "config" / "agent_prompts.yaml"
KNOWLEDGE_PATH = Path(__file__).parent.parent / "knowledge"


def _load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_knowledge() -> str:
    """Concatena todos os arquivos da base de conhecimento."""
    docs = []
    for md_file in sorted(KNOWLEDGE_PATH.glob("*.md")):
        docs.append(f"## {md_file.stem.upper()}\n\n{md_file.read_text(encoding='utf-8')}")
    return "\n\n---\n\n".join(docs)


class BaseAgent:
    """Agente base com integração Anthropic e base de conhecimento Finlancer."""

    agent_key: str = ""  # Sobrescrever nas subclasses

    def __init__(self, client: Anthropic):
        self.client = client
        config = _load_config()
        agent_config = config["agents"][self.agent_key]
        self.name = agent_config["name"]
        self.model = agent_config["model"]
        self.temperature = agent_config["temperature"]
        self.max_tokens = agent_config["max_tokens"]
        self._system_prompt_template = agent_config["system_prompt"]
        self._retry_config = config.get("retry_config", {})
        self._knowledge = _load_knowledge()
        self.conversation_history: list[dict] = []

    @property
    def system_prompt(self) -> str:
        return (
            self._system_prompt_template
            + "\n\n---\n\n## BASE DE CONHECIMENTO FINLANCER\n\n"
            + self._knowledge
        )

    def run(self, user_message: str, reset_history: bool = False, model: str = None) -> str:
        """Envia mensagem e retorna resposta do agente."""
        if reset_history:
            self.conversation_history = []

        self.conversation_history.append({"role": "user", "content": user_message})

        max_retries = self._retry_config.get("max_retries", 3)
        delay = self._retry_config.get("retry_delay_seconds", 2)

        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=model or self.model,
                    max_tokens=self.max_tokens,
                    system=[{
                        "type": "text",
                        "text": self.system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    messages=self.conversation_history,
                )
                content = response.content[0].text
                self.conversation_history.append({"role": "assistant", "content": content})
                logger.info(f"[{self.name}] Resposta gerada ({len(content)} chars)")
                return content

            except Exception as e:
                logger.warning(f"[{self.name}] Tentativa {attempt + 1} falhou: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2**attempt))
                else:
                    raise

        return ""

    def reset(self) -> None:
        self.conversation_history = []
