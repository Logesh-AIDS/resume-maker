"""
Factory that instantiates the correct LLMProvider based on config.
Single import point — all services use get_llm_provider().
"""
from functools import lru_cache

from src.ai.base import LLMProvider
from src.core.config import get_settings
from src.core.exceptions import AIServiceError
from src.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    """
    Return a cached LLMProvider instance.
    Provider is chosen by LLM_PROVIDER env var (default: gemini).
    """
    settings = get_settings()
    provider_name = settings.llm_provider

    if provider_name == "gemini":
        from src.ai.gemini_provider import GeminiProvider
        provider = GeminiProvider()
        logger.info("llm_provider_initialized", provider="gemini", model=provider.model_name)
        return provider

    if provider_name == "openai":
        from src.ai.openai_provider import OpenAIProvider
        provider = OpenAIProvider()
        logger.info("llm_provider_initialized", provider="openai", model=provider.model_name)
        return provider

    raise AIServiceError(
        f"Unknown LLM provider: '{provider_name}'. "
        "Supported values: 'gemini', 'openai'."
    )
