"""Application-specific exceptions.

Using dedicated exception types (instead of catching bare ``Exception``
everywhere) keeps error handling explicit and satisfies static-analysis
rules such as Ruff's BLE001 and SonarQube's generic-exception-catch check.
"""

from __future__ import annotations


class FoodAnalyzerError(Exception):
    """Base class for all errors raised by this application."""


class VisionProviderError(FoodAnalyzerError):
    """Raised when the external vision AI provider call fails."""


class NutritionParsingError(FoodAnalyzerError):
    """Raised when the vision provider's response cannot be parsed."""
