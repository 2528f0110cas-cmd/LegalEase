"""FastAPI application entry point."""
from __future__ import annotations
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router

load_dotenv()

app = FastAPI(title="LegalEase API", description="AI-assisted legal document drafting API.", version="1.0.0")

allowed_origins = [x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:8501,http://127.0.0.1:8501").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=False, allow_methods=["GET","POST"], allow_headers=["*"])

@app.get("/")
def root():
    return {"name":"LegalEase API","status":"running","docs":"/docs"}

@app.get("/health")
def health():
    mock = os.getenv("MOCK_AI","true").strip().lower() in {"1","true","yes","on"}
    return {"status":"ok","mock_ai":mock,"model":os.getenv("GEMINI_MODEL","gemini-3.8-flash")}

app.include_router(router)
