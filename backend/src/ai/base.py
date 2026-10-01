"""
LLM Provider abstraction.

All AI services depend on LLMProvider — never on a specific SDK directly.
This allows swapping Gemini ↔ OpenAI ↔ Anthropic via config with zero code change.

Design rules:
  - Document content (JD text, resume text) is always passed as DATA.
  - System prompts contain ONLY application instructions, never user-supplied content.
  - All outputs are validated via Pydantic before use.
  - Retries are handled internally with tenacity.
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMMessage:
    """A single message in a prompt conversation."""

    __slots__ = ("role", "content")

    def __init__(self, role: str, content: str) -> None:
        self.role = role       # "system" | "user" | "assistant"
        self.content = content

    @classmethod
    def system(cls, content: str) -> "LLMMessage":
        return cls("system", content)

    @classmethod
    def user(cls, content: str) -> "LLMMessage":
        return cls("user", content)

    @classmethod
    def assistant(cls, content: str) -> "LLMMessage":
        return cls("assistant", content)


class LLMResponse:
    """Parsed response from the LLM."""

    __slots__ = ("text", "input_tokens", "output_tokens", "model")

    def __init__(
        self,
        text: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        model: str = "",
    ) -> None:
        self.text = text
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.model = model


class LLMProvider(ABC):
    """
    Abstract base for all LLM providers.

    Concrete providers must implement `complete` and `complete_json`.
    `complete_json` returns a validated Pydantic model parsed from JSON output.
    """

    @abstractmethod
    async def complete(
        self,
        messages: list[LLMMessage],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Send messages and return free-text response."""
        ...

    @abstractmethod
    async def complete_json(
        self,
        messages: list[LLMMessage],
        schema: type[T],
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> T:
        """
        Send messages and return a validated Pydantic model.
        The provider is responsible for instructing the LLM to output valid JSON
        and for retrying on parse failures.
        """
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier string."""
        ...
