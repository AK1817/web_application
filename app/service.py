"""Service layer: orchestrates use cases independent of any web framework.

Keeping this logic out of the FastAPI route functions makes it directly
unit-testable without spinning up an HTTP client, and keeps route
functions thin (a SonarQube maintainability signal).
"""

from __future__ import annotations

from app.models import NutritionEstimate
from app.vision.base import VisionClient


class FoodAnalysisService:
    """Coordinates food image analysis via an injected VisionClient."""

    def __init__(self, vision_client: VisionClient) -> None:
        """Initialize the service.

        Args:
            vision_client: Any VisionClient implementation. Injected rather
                than constructed here, so tests can supply a fake.
        """
        self._vision_client = vision_client

    def analyze_food_image(
        self, image_bytes: bytes, media_type: str
    ) -> NutritionEstimate:
        """Analyze a food image and return its nutrition estimate.

        Args:
            image_bytes: Raw bytes of the uploaded image.
            media_type: MIME type of the image.

        Returns:
            A validated NutritionEstimate.
        """
        return self._vision_client.analyze(image_bytes, media_type)
