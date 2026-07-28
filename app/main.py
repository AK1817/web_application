"""FastAPI application: routes only, wired via dependency injection.

Run with:
    uvicorn app.main:app --reload
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import Settings, load_settings
from app.exceptions import FoodAnalyzerError
from app.service import FoodAnalysisService
from app.vision.gemini import GeminiVisionClient

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parent
_DEFAULT_CONFIDENCE = "unknown"

app = FastAPI(title="Food Nutrition Analyzer")
templates = Jinja2Templates(directory=str(_BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(_BASE_DIR / "static")), name="static")


@lru_cache
def get_settings() -> Settings:
    """Provide a cached Settings instance for dependency injection."""
    return load_settings()


def get_food_analysis_service(
    settings: Settings = Depends(get_settings),
) -> FoodAnalysisService:
    """Build a FoodAnalysisService wired to the Gemini vision client."""
    vision_client = GeminiVisionClient(
        api_key=settings.gemini_api_key,
        api_url=settings.gemini_api_url,
        timeout_seconds=settings.request_timeout_seconds,
    )
    return FoodAnalysisService(vision_client)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Render the upload page."""
    return templates.TemplateResponse(request, "index.html", {})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_food(
    request: Request,
    file: UploadFile = File(...),
    service: FoodAnalysisService = Depends(get_food_analysis_service),
) -> HTMLResponse:
    """Accept an uploaded food image and render its nutrition estimate."""
    image_bytes = await file.read()
    media_type = file.content_type or "image/jpeg"

    context: dict[str, object] = {"error": None}

    try:
        estimate = service.analyze_food_image(image_bytes, media_type)
    except FoodAnalyzerError as exc:
        logger.warning("Food analysis failed: %s", exc)
        context["error"] = str(exc)
    else:
        context.update(
            {
                "food_name": estimate.food_name,
                "calories": estimate.calories,
                "protein": estimate.protein_g,
                "carbs": estimate.carbs_g,
                "fat": estimate.fat_g,
                "confidence": estimate.confidence.value,
            }
        )

    return templates.TemplateResponse(request, "result.html", context)
