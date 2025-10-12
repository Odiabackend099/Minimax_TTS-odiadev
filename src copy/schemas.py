"""Pydantic schemas (skeleton)."""
from __future__ import annotations
try:
    from pydantic import BaseModel
except Exception:
    class BaseModel:  # type: ignore
        pass

class HealthResponse(BaseModel):
    status: str
