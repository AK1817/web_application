"""Domain models used across the application."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Confidence(StrEnum):
    """How confident the vision model is in its nutrition estimate."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class NutritionEstimate(BaseModel):
    """A structured nutrition estimate produced by a vision AI provider."""

    food_name: str = Field(..., description="Identified food or dish name.")
    calories: float = Field(..., ge=0, description="Estimated calories (kcal).")
    protein_g: float = Field(..., ge=0, description="Estimated protein in grams.")
    carbs_g: float = Field(..., ge=0, description="Estimated carbohydrates in grams.")
    fat_g: float = Field(..., ge=0, description="Estimated fat in grams.")
    confidence: Confidence = Field(
        default=Confidence.MEDIUM,
        description="Model's self-reported confidence in the estimate.",
    )
