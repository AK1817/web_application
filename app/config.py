"""Application configuration.

Centralizes all environment-driven settings so no other module reads
``os.environ`` directly.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

_DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-lite"
_DEFAULT_REQUEST_TIMEOUT_SECONDS = 60


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable application settings.

    Attributes:
        gemini_api_key: API key for the Gemini API. Required at runtime.
        gemini_model: Which Gemini model to call.
        request_timeout_seconds: HTTP timeout used for outbound API calls.
    """

    gemini_api_key: str | None
    gemini_model: str
    request_timeout_seconds: int

    @property
    def gemini_api_url(self) -> str:
        """Build the full Gemini `generateContent` endpoint URL."""
        return (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.gemini_model}:generateContent"
        )


def load_settings() -> Settings:
    """Load settings from environment variables.

    Returns:
        A populated, immutable Settings instance.
    """
    return Settings(
        gemini_api_key=os.environ.get("GEMINI_API_KEY"),
        gemini_model=os.environ.get("GEMINI_MODEL", _DEFAULT_GEMINI_MODEL),
        request_timeout_seconds=int(
            os.environ.get("REQUEST_TIMEOUT_SECONDS", _DEFAULT_REQUEST_TIMEOUT_SECONDS)
        ),
    )
