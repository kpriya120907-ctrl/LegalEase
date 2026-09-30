from typing import Optional

from backend.app.config import settings
from backend.app.utils.text import sanitize_text


class GeminiDocumentGenerator:

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):

        self.api_key = (
            api_key or settings.GEMINI_API_KEY
        )

        self.model_name = (
            model_name or settings.GEMINI_MODEL
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured. "
                "Please add it to your .env file."
            )

        try:
            from google import genai

        except ImportError as exc:

            raise RuntimeError(
                "google-genai is not installed. "
                "Run: pip install google-genai"
            ) from exc

        self.client = genai.Client(
            api_key=self.api_key
        )

    def build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        additional_instructions: str = "",
    ) -> str:

        return f"""
You are a professional legal-document drafting assistant.

Create a structured legal-document DRAFT.

IMPORTANT:
- This is an AI-generated draft.
- Do not invent facts.
- Do not invent names, dates, amounts or laws.
- If information is missing, use [NOT PROVIDED].
- Use professional and neutral legal language.
- Use clear headings and numbered sections.
- Do not claim that the document is legally valid in every jurisdiction.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE / RELEVANT DATES:
{dates}

TERMS AND CONDITIONS:
{terms}

ADDITIONAL INSTRUCTIONS:
{additional_instructions or "[None provided]"}

Include relevant sections such as:

1. PURPOSE
2. DEFINITIONS
3. SCOPE / RESPONSIBILITIES
4. TERMS AND CONDITIONS
5. PAYMENT, IF APPLICABLE
6. CONFIDENTIALITY, IF APPLICABLE
7. TERM AND TERMINATION
8. OBLIGATIONS
9. DISPUTE / GOVERNING LAW, ONLY IF DETAILS WERE PROVIDED
10. GENERAL PROVISIONS
11. SIGNATURES

At the end include:

IMPORTANT NOTICE

This document is an AI-generated draft and should be reviewed
by a qualified legal professional before being signed or relied upon.

Return only the document draft.
"""

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        additional_instructions: str = "",
    ) -> str:

        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            dates=dates,
            additional_instructions=additional_instructions,
        )

        try:

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini API request failed: {exc}"
            ) from exc

        generated_text = getattr(
            response,
            "text",
            None,
        )

        if not generated_text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        generated_text = sanitize_text(
            generated_text
        )

        if len(generated_text) > settings.MAX_DOCUMENT_LENGTH:

            generated_text = generated_text[
                :settings.MAX_DOCUMENT_LENGTH
            ]

        return generated_text