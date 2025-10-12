"""Database setup for OdeaDev‑AI‑TTS."""
from __future__ import annotations
import os
from contextlib import contextmanager

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
except Exception:
    create_engine = None  # type: ignore
    sessionmaker = None   # type: ignore

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./odeadev_tts.db")

if create_engine:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

@contextmanager
def get_session():
    if SessionLocal is None:
        raise RuntimeError("SQLAlchemy not available in this environment")
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
