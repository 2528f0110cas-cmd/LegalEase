"""FastAPI routes for LegalEase."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator
from services.text_utils import parse_terms, sanitize_text

router = APIRouter()

class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=120)
    parties: str = Field(min_length=2, max_length=5000)
    terms: str = Field(min_length=2, max_length=10000)
    effective_date: str = Field(min_length=2, max_length=100)

class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    mock: bool

generator = GeminiDocumentGenerator()

@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    document_type = sanitize_text(request.document_type)
    parties = sanitize_text(request.parties)
    terms = parse_terms(request.terms)
    effective_date = sanitize_text(request.effective_date)
    if not terms:
        raise HTTPException(status_code=422, detail="At least one term is required.")
    try:
        result = generator.generate_document(document_type, parties, terms, effective_date)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return DocumentResponse(document_type=document_type, content=sanitize_text(result.content), model=result.model, mock=result.mock)
