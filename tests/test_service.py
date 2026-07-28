"""Unit tests for FoodAnalysisService.

Because the service depends on the VisionClient abstraction rather than
a concrete provider, it can be tested with a fake, with no network calls.
"""

from __future__ import annotations

from app.models import Confidence, NutritionEstimate
from app.service import FoodAnalysisService
from app.vision.base import VisionClient


class _FakeVisionClient(VisionClient):
    """A stub VisionClient returning a fixed estimate, for tests only."""

    def analyze(self, _image_bytes: bytes, _media_type: str) -> NutritionEstimate:
        """Return a canned nutrition estimate regardless of input."""
        return NutritionEstimate(
            food_name="Apple",
            calories=95,
            protein_g=0.5,
            carbs_g=25,
            fat_g=0.3,
            confidence=Confidence.HIGH,
        )


def test_analyze_food_image_returns_estimate_from_client() -> None:
    """The service should return exactly what the injected client returns."""
    service = FoodAnalysisService(vision_client=_FakeVisionClient())

    result = service.analyze_food_image(
        image_bytes=b"fake-bytes", media_type="image/jpeg"
    )

    assert result.food_name == "Apple"
    assert result.calories == 95
    assert result.confidence == Confidence.HIGH
