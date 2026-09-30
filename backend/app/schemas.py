from typing import Optional

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=500
    )

    additional_instructions: Optional[str] = Field(
        default="",
        max_length=5000
    )


class DocumentResponse(BaseModel):

    success: bool

    document_type: str

    content: str

    message: str


class HealthResponse(BaseModel):

    status: str

    service: str

    version: str