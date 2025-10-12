"""SQLAlchemy ORM models for OdeaDev-AI-TTS."""
from __future__ import annotations
from datetime import datetime

try:
    from sqlalchemy.orm import declarative_base, relationship
    from sqlalchemy import (
        Column, Integer, String, DateTime, Boolean, Float, 
        ForeignKey, Text, Enum as SQLEnum
    )
    import enum
except Exception:
    declarative_base = lambda: None  # type: ignore
    relationship = None
    Column = Integer = String = DateTime = Boolean = Float = None
    ForeignKey = Text = SQLEnum = None
    enum = None

Base = declarative_base() if callable(declarative_base) else None


class Plan(enum.Enum if enum else object):
    """Billing plan tiers."""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class Gender(enum.Enum if enum else object):
    """Voice gender options."""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class UsageStatus(enum.Enum if enum else object):
    """TTS request status."""
    SUCCESS = "success"
    ERROR = "error"
    QUOTA_EXCEEDED = "quota_exceeded"
    RATE_LIMITED = "rate_limited"


class User(Base if Base else object):
    """User account with API key and quota management."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    api_key_hash = Column(String(64), unique=True, nullable=False)  # SHA256 hash
    plan = Column(SQLEnum(Plan), default=Plan.FREE, nullable=False)
    quota_seconds = Column(Float, default=600.0, nullable=False)  # 10 min for free
    used_seconds = Column(Float, default=0.0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    usage_logs = relationship("Usage", back_populates="user", cascade="all, delete-orphan")

    @property
    def remaining_seconds(self) -> float:
        """Calculate remaining quota."""
        return max(0.0, self.quota_seconds - self.used_seconds)

    @property
    def quota_percentage_used(self) -> float:
        """Percentage of quota consumed."""
        if self.quota_seconds == 0:
            return 100.0
        return min(100.0, (self.used_seconds / self.quota_seconds) * 100)


class Voice(Base if Base else object):
    """Voice mapping between friendly names and MiniMax voice IDs."""
    __tablename__ = "voices"

    id = Column(Integer, primary_key=True, index=True)
    friendly_name = Column(String(100), unique=True, index=True, nullable=False)
    minimax_voice_id = Column(String(255), nullable=False)
    language = Column(String(10), nullable=False)  # e.g., "en-US", "en-NG", "en-GB"
    gender = Column(SQLEnum(Gender), nullable=False)
    description = Column(Text, nullable=True)
    is_cloned = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    usage_logs = relationship("Usage", back_populates="voice")


class Usage(Base if Base else object):
    """Usage log for TTS requests."""
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    voice_id = Column(Integer, ForeignKey("voices.id"), nullable=True)
    text_length = Column(Integer, nullable=False)  # Character count
    audio_seconds = Column(Float, nullable=True)  # Actual audio duration
    status = Column(SQLEnum(UsageStatus), nullable=False)
    error_message = Column(Text, nullable=True)
    model_used = Column(String(50), nullable=True)  # e.g., "speech-02-hd"
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="usage_logs")
    voice = relationship("Voice", back_populates="usage_logs")


# Plan quotas configuration (not a DB table, just reference)
PLAN_CONFIGS = {
    Plan.FREE: {
        "price": 0,
        "quota_seconds": 600,  # 10 minutes
        "rpm": 10,
        "max_streams": 1,
    },
    Plan.BASIC: {
        "price": 19,
        "quota_seconds": 3600,  # 60 minutes
        "rpm": 30,
        "max_streams": 2,
    },
    Plan.PRO: {
        "price": 70,
        "quota_seconds": 14400,  # 240 minutes
        "rpm": 60,
        "max_streams": 5,
    },
    Plan.ENTERPRISE: {
        "price": 180,
        "quota_seconds": 36000,  # 600 minutes (customizable)
        "rpm": 120,
        "max_streams": 10,
    },
}
