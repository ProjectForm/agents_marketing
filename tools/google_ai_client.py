import os
import logging

logger = logging.getLogger(__name__)

_google_client = None


def get_google_client():
    """Returns a cached Google AI (genai) client. Raises if key is missing."""
    global _google_client
    if _google_client is not None:
        return _google_client

    try:
        from google import genai
    except ImportError:
        raise ImportError(
            "Pacote 'google-genai' não instalado. Execute: pip install google-genai"
        )

    api_key = os.environ.get("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_AI_API_KEY não encontrada. Configure no arquivo .env"
        )

    _google_client = genai.Client(api_key=api_key)
    logger.info("Google AI client inicializado.")
    return _google_client
