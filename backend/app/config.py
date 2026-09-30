import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:

    APP_NAME = "LegalEase"
    APP_VERSION = "1.0.0"

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:8501"
    )

    MAX_DOCUMENT_LENGTH = int(
        os.getenv(
            "MAX_DOCUMENT_LENGTH",
            "30000"
        )
    )


settings = Settings()