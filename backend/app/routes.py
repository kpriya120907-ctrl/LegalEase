from fastapi import APIRouter, HTTPException

from backend.app.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.app.schemas import (
    DocumentRequest,
    DocumentResponse,
)
from backend.app.config import settings


router = APIRouter()


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
def generate_document(request: DocumentRequest):
    """
    Generate a legal document using Gemini.
    """

    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail=(
                "Gemini API key is not configured. "
                "Please add GEMINI_API_KEY to .env."
            ),
        )

    try:

        generator = GeminiDocumentGenerator()

        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
            additional_instructions=(
                request.additional_instructions or ""
            ),
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=content,
            message="Document generated successfully.",
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {exc}",
        ) from exc