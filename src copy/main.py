"""Entry point for the OdeaDev‑AI‑TTS service.

A minimal FastAPI app with a health check endpoint.
"""
from __future__ import annotations
import os

try:
    from fastapi import FastAPI
except Exception:
    # Allow import even if FastAPI isn't installed in this environment.
    FastAPI = None  # type: ignore

app = FastAPI(title="OdeaDev‑AI‑TTS", version="0.1.0") if FastAPI else None

if app:
    @app.get("/health")
    def health():
        return {"status": "ok"}

__all__ = ["app"]
