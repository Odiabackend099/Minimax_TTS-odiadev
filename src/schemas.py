"""Pydantic schemas for request/response validation."""
from __future__ import annotations
from datetime import datetime
from typing import Optional

try:
    from pydantic import BaseModel, EmailStr, Field, ConfigDict
except Exception:
    class BaseModel:  # type: ignore
        pass
    EmailStr = str
    Field = lambda *args, **kwargs: None
    ConfigDict = dict


# ==================== Health ====================
class HealthResponse(BaseModel):
    status: str


# ==================== User Schemas ====================
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    plan: str = Field(default="free", pattern="^(free|basic|pro|enterprise)$")


class UserResponse(BaseModel):
    """Schema for user data in responses."""
    id: int
    name: str
    email: str
    plan: str
    quota_seconds: float
    used_seconds: float
    remaining_seconds: float
    quota_percentage_used: float
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreateResponse(BaseModel):
    """Response when creating a user - includes plain API key once."""
    user: UserResponse
    api_key: str  # Plain key, shown only once!


class QuotaUpdate(BaseModel):
    """Schema for updating user quota."""
    quota_seconds: Optional[float] = Field(None, ge=0)
    used_seconds: Optional[float] = Field(None, ge=0)


# ==================== Voice Schemas ====================
class VoiceCreate(BaseModel):
    """Schema for registering a new voice."""
    friendly_name: str = Field(..., min_length=1, max_length=100)
    minimax_voice_id: str = Field(..., min_length=1)
    language: str = Field(..., pattern="^[a-z]{2}-[A-Z]{2}$")  # e.g., en-US
    gender: str = Field(..., pattern="^(male|female|neutral)$")
    description: Optional[str] = None
    is_cloned: bool = False


class VoiceResponse(BaseModel):
    """Schema for voice data in responses."""
    id: int
    friendly_name: str
    language: str
    gender: str
    description: Optional[str]
    is_cloned: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== TTS Request/Response ====================
class TTSRequest(BaseModel):
    """Schema for TTS generation request."""
    text: str = Field(..., min_length=1, max_length=5000)
    voice_name: Optional[str] = Field(None, description="Friendly voice name")
    model: str = Field(default="speech-02-turbo", pattern="^speech-0[12]-(hd|turbo).*$")
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    pitch: int = Field(default=0, ge=-12, le=12)
    emotion: str = Field(
        default="neutral",
        pattern="^(neutral|happy|sad|angry|fearful|disgusted|surprised)$"
    )


class TTSResponse(BaseModel):
    """Schema for TTS generation response."""
    audio_base64: str
    duration_seconds: float
    sample_rate: int
    voice_used: str
    text_length: int
    remaining_quota: float


# ==================== Usage/Stats ====================
class UsageStats(BaseModel):
    """Schema for usage statistics."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_audio_seconds: float
    quota_used_percentage: float


class UsageLogResponse(BaseModel):
    """Schema for individual usage log entry."""
    id: int
    text_length: int
    audio_seconds: Optional[float]
    status: str
    error_message: Optional[str]
    model_used: Optional[str]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
