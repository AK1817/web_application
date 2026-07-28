# Food Nutrition Analyzer

A simple web app that estimates the nutrition content (calories, protein, carbs, fat) of a food photo using Google's Gemini AI.

Upload a photo of your meal, and the app identifies the food and returns an estimated nutrition breakdown — built with FastAPI and Google's Gemini vision API.

## Features

- Upload a food photo through a simple web form
- Get an estimated food name, calories, protein, carbs, and fat
- Powered by Google Gemini's free-tier vision API (no cost to run)
- Clean, class-based backend structure (FastAPI + dependency injection)

## Tech Stack

- **Backend:** FastAPI (Python)
- **AI Vision:** Google Gemini API (`gemini-3.1-flash-lite`)
- **Templating:** Jinja2
- **Package management:** [uv](https://github.com/astral-sh/uv)
- **Linting:** Ruff

## Project Structure

```
web_application/
├── app/
│   ├── main.py           # FastAPI routes
│   ├── config.py         # Environment/settings loader
│   ├── models.py         # Pydantic data models
│   ├── service.py         # Business logic layer
│   ├── exceptions.py      # Custom exception types
│   ├── vision/
│   │   ├── base.py        # Abstract VisionClient interface
│   │   └── gemini.py      # Gemini API implementation
│   ├── templates/         # HTML pages (Jinja2)
│   └── static/            # CSS styling
├── tests/
│   └── test_service.py
├── pyproject.toml         # Ruff config + project metadata
└── requirements.txt
```

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/AK1817/web_application.git
cd web_application
```

### 2. Install dependencies
```bash
uv add fastapi "uvicorn[standard]" python-multipart jinja2 requests pydantic
uv add --dev ruff pytest
```

### 3. Get a free Gemini API key
1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with a Google account (no credit card required)
3. Click **Create API key** and copy it

### 4. Set your API key
```powershell
$env:GEMINI_API_KEY="your-key-here"
```

### 5. Run the app
```bash
uv run uvicorn app.main:app --reload
```

Then open **http://127.0.0.1:8000** in your browser.

## Running Tests & Lint Checks
```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

## Notes

- Uses Gemini's free tier — no billing required, but subject to daily/rate limits.
- Nutrition values are AI-estimated and not medically precise; don't rely on them for medical or dietary decision-making.

## License

This project is for personal/educational use.
