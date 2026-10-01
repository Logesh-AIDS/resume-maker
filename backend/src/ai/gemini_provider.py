"""
Google Gemini provider (gemini-1.5-flash — free tier default).

Free tier limits (as of 2024):
  - 15 requests/min
  - 1,000,000 tokens/day
  - No credit card required

Structured JSON output uses Gemini's response_mime_type="application/json"
with a response_schema for reliable parsing.
"""
import json
import re
from typing import TypeVar

import google.generativeai as genai
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


def _messages_to_gemini(
    messages: list[LLMMessage],
) -> tuple[str, list[dict]]:
    """
    Gemini uses a system_instruction + contents format.
    Returns (system_instruction, contents).
    """
    system_parts: list[str] = []
    contents: list[dict] = []

    for msg in messages:
        if msg.role == "system":
            system_parts.append(msg.content)
        elif msg.role == "user":
            contents.append({"role": "user", "parts": [{"text": msg.content}]})
        elif msg.role == "assistant":
            contents.append({"role": "model", "parts": [{"text": msg.content}]})

    return "\n\n".join(system_parts), contents


class GeminiProvider(LLMProvider):
    """Gemini 1.5 Flash provider — free-tier default."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise AIServiceError(
                "GEMINI_API_KEY is not configured. "
                "Set it in your .env file. Get a free key at https://aistudio.google.com/"
            )
        genai.configure(api_key=settings.gemini_api_key)
        self._model_id = settings.gemini_model

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
        system_instruction, contents = _messages_to_gemini(messages)

        try:
            model = genai.GenerativeModel(
                model_name=self._model_id,
                system_instruction=system_instruction or None,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            response = model.generate_content(contents)
            text = response.text or ""

            return LLMResponse(
                text=text,
                input_tokens=getattr(response.usage_metadata, "prompt_token_count", 0),
                output_tokens=getattr(response.usage_metadata, "candidates_token_count", 0),
                model=self._model_id,
            )
        except Exception as exc:
            logger.error("gemini_complete_failed", error=str(exc), model=self._model_id)
            raise AIServiceError(f"Gemini API error: {exc}") from exc

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
        """
        Request JSON output from Gemini and parse into a Pydantic model.
        Uses response_mime_type=application/json for reliable structured output.
        Falls back to regex JSON extraction on parse failure.
        """
        system_instruction, contents = _messages_to_gemini(messages)

        # Append schema hint to system instruction for best JSON adherence
        schema_hint = (
            f"\n\nYou MUST respond with valid JSON only. "
            f"No markdown, no explanation. "
            f"The JSON must conform to this structure: {json.dumps(schema.model_json_schema(), indent=2)}"
        )

        try:
            model = genai.GenerativeModel(
                model_name=self._model_id,
                system_instruction=(system_instruction or "") + schema_hint,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    response_mime_type="application/json",
                ),
            )
            response = model.generate_content(contents)
            raw = response.text or "{}"

            # Strip markdown fences if present (safety net)
            raw = _strip_json_fences(raw)

            parsed = schema.model_validate_json(raw)
            logger.debug(
                "gemini_json_complete",
                schema=schema.__name__,
                output_tokens=getattr(response.usage_metadata, "candidates_token_count", 0),
            )
            return parsed

        except (json.JSONDecodeError, ValidationError) as exc:
            logger.warning("gemini_json_parse_failed", schema=schema.__name__, error=str(exc))
            raise  # tenacity will retry

        except Exception as exc:
            logger.error("gemini_json_failed", schema=schema.__name__, error=str(exc))
            raise AIServiceError(f"Gemini JSON completion failed: {exc}") from exc


def _strip_json_fences(text: str) -> str:
    """Remove ```json ... ``` or ``` ... ``` wrappers if present."""
    text = text.strip()
    match = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text)
    if match:
        return match.group(1).strip()
    return text
