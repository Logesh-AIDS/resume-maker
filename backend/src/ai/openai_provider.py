"""
OpenAI provider (gpt-4o-mini by default — lowest cost option).
Falls back provider — only used if LLM_PROVIDER=openai in .env.
"""
import json
from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.ai.base import LLMMessage, LLMProvider, LLMResponse
from src.core.config import get_settings
from src.core.exceptions import AIServiceError
from src.core.logging import get_logger

logger = get_logger(__name__)
T = TypeVar("T", bound=BaseModel)
settings = get_settings()


def _messages_to_openai(messages: list[LLMMessage]) -> list[dict]:
    return [{"role": m.role, "content": m.content} for m in messages]


class OpenAIProvider(LLMProvider):
    """OpenAI provider using gpt-4o-mini."""

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise AIServiceError(
                "OPENAI_API_KEY is not configured. Set it in your .env file."
            )
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model_id = settings.openai_model

    @property
    def model_name(self) -> str:
        return self._model_id

    @retry(
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def complete(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        try:
            response = await self._client.chat.completions.create(
                model=self._model_id,
                messages=_messages_to_openai(messages),  # type: ignore[arg-type]
                temperature=temperature,
                max_tokens=max_tokens,
            )
            text = response.choices[0].message.content or ""
            return LLMResponse(
                text=text,
                input_tokens=response.usage.prompt_tokens if response.usage else 0,
                output_tokens=response.usage.completion_tokens if response.usage else 0,
                model=self._model_id,
            )
        except Exception as exc:
            logger.error("openai_complete_failed", error=str(exc))
            raise AIServiceError(f"OpenAI API error: {exc}") from exc

    @retry(
        retry=retry_if_exception_type((json.JSONDecodeError, ValidationError)),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        stop=stop_after_attempt(3),
        reraise=False,
    )
    async def complete_json(
        self,
        messages: list[LLMMessage],
        schema: type[T],
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> T:
        try:
            response = await self._client.chat.completions.create(
                model=self._model_id,
                messages=_messages_to_openai(messages),  # type: ignore[arg-type]
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or "{}"
            return schema.model_validate_json(raw)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.warning("openai_json_parse_failed", schema=schema.__name__, error=str(exc))
            raise
        except Exception as exc:
            logger.error("openai_json_failed", schema=schema.__name__, error=str(exc))
            raise AIServiceError(f"OpenAI JSON completion failed: {exc}") from exc
