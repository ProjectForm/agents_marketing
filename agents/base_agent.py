import os
import time
import logging
import yaml
from pathlib import Path
from google import genai
from google.genai import types

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
    """Agente base com integração Gemini e base de conhecimento Finlancer."""

    agent_key: str = ""  # Sobrescrever nas subclasses

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model_name
        config = _load_config()
        agent_config = config["agents"][self.agent_key]
        self.name = agent_config["name"]
        self.temperature = agent_config["temperature"]
        self.max_tokens = 8192 # Force higher max_tokens for all agents to prevent truncation
        self._system_prompt_template = agent_config["system_prompt"]
        self._retry_config = config.get("retry_config", {})
        self._knowledge = _load_knowledge()
        
        self.config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens,
        )

    @property
    def system_prompt(self) -> str:
        return (
            self._system_prompt_template
            + "\n\n---\n\n## BASE DE CONHECIMENTO FINLANCER\n\n"
            + self._knowledge
        )

    def run(self, prompt: str, reset_history: bool = False) -> str:
        """Envia mensagem e retorna resposta do agente."""
        max_retries = self._retry_config.get("max_retries", 3)
        delay = self._retry_config.get("retry_delay_seconds", 2)

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=self.config
                )
                content = response.text
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
        # O novo SDK não mantém chat state automaticamente da mesma forma, 
        # mas para o uso atual de 'run' simples, isso não é estritamente necessário.
        pass
