"""Gemini implementation of the VisionClient interface."""

from __future__ import annotations

import base64
import json
import logging
from typing import Any, Final

import requests
from pydantic import ValidationError

from app.exceptions import NutritionParsingError, VisionProviderError
from app.models import NutritionEstimate
from app.vision.base import VisionClient

logger = logging.getLogger(__name__)

_ANALYSIS_PROMPT: Final[str] = (
    "You are a nutrition estimation assistant. Look at the food in this "
    "image and identify it, then estimate its nutritional content. "
    "Respond with ONLY a JSON object (no markdown, no extra text) in "
    "exactly this format:\n"
    '{"food_name": "string", "calories": number, "protein_g": number, '
    '"carbs_g": number, "fat_g": number, "confidence": "high|medium|low"}'
)

_MARKDOWN_FENCE: Final[str] = "```"


class GeminiVisionClient(VisionClient):
    """Vision client backed by Google's Gemini API (free tier compatible)."""

    def __init__(self, api_key: str | None, api_url: str, timeout_seconds: int) -> None:
        """Initialize the client.

        Args:
            api_key: Gemini API key. May be None, in which case calls fail
                fast with a clear error rather than an opaque 401 later.
            api_url: Full Gemini `generateContent` endpoint URL.
            timeout_seconds: HTTP request timeout.
        """
        self._api_key = api_key
        self._api_url = api_url
        self._timeout_seconds = timeout_seconds

    def analyze(self, image_bytes: bytes, media_type: str) -> NutritionEstimate:
        """Send an image to Gemini and return a parsed NutritionEstimate."""
        if not self._api_key:
            raise VisionProviderError(
                "GEMINI_API_KEY is not set. Get a free key at "
                "https://aistudio.google.com/apikey"
            )

        raw_text = self._call_gemini(image_bytes, media_type)
        return self._parse_response(raw_text)

    def _call_gemini(self, image_bytes: bytes, media_type: str) -> str:
        """Perform the HTTP call to Gemini and return the raw text reply."""
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload: dict[str, Any] = {
            "contents": [
                {
                    "parts": [
                        {"text": _ANALYSIS_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": media_type,
                                "data": image_b64,
                            }
                        },
                    ]
                }
            ]
        }

        try:
            response = requests.post(
                self._api_url,
                headers={
                    "content-type": "application/json",
                    "x-goog-api-key": self._api_key,
                },
                json=payload,
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.exception("Gemini API request failed")
            raise VisionProviderError(f"Gemini API request failed: {exc}") from exc

        return self._extract_text(response.json())

    @staticmethod
    def _extract_text(response_json: dict[str, Any]) -> str:
        """Pull the model's text reply out of a Gemini response payload."""
        try:
            candidates = response_json["candidates"]
            parts = candidates[0]["content"]["parts"]
            return str(parts[0]["text"])
        except (KeyError, IndexError, TypeError) as exc:
            logger.exception("Unexpected Gemini response shape")
            raise NutritionParsingError(
                "Gemini response did not contain expected content."
            ) from exc

    @staticmethod
    def _parse_response(raw_text: str) -> NutritionEstimate:
        """Parse Gemini's raw text reply into a validated NutritionEstimate."""
        cleaned = raw_text.strip()
        if cleaned.startswith(_MARKDOWN_FENCE):
            cleaned = cleaned.strip(_MARKDOWN_FENCE)
            cleaned = cleaned.removeprefix("json").strip()

        try:
            payload = json.loads(cleaned)
            return NutritionEstimate.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.exception("Failed to parse Gemini nutrition JSON")
            raise NutritionParsingError(
                f"Could not parse nutrition data from model response: {exc}"
            ) from exc
