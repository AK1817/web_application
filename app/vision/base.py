"""Abstract contract that every vision AI provider must implement.

Defining this interface means the FastAPI route layer depends only on
``VisionClient``, never on a specific provider. Swapping Gemini for
another provider (e.g. LogMeal, GPT-4V) means adding one new subclass,
with no changes required anywhere else.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import NutritionEstimate


class VisionClient(ABC):
    """Interface for a vision AI provider that estimates food nutrition."""

    @abstractmethod
    def analyze(self, image_bytes: bytes, media_type: str) -> NutritionEstimate:
        """Analyze a food image and return a structured nutrition estimate.

        Args:
            image_bytes: Raw bytes of the uploaded image.
            media_type: MIME type of the image, e.g. ``"image/jpeg"``.

        Returns:
            A validated NutritionEstimate.

        Raises:
            VisionProviderError: If the underlying API call fails.
            NutritionParsingError: If the response cannot be parsed.
        """
        raise NotImplementedError
