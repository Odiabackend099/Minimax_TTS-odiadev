"""Production-ready database setup with connection pooling and health checks."""
from __future__ import annotations
import os
from contextlib import contextmanager
from typing import Generator

try:
    from sqlalchemy import create_engine, event, select
    from sqlalchemy.orm import sessionmaker, Session
    from sqlalchemy.pool import QueuePool, NullPool
    from sqlalchemy.exc import SQLAlchemyError
except Exception:
    create_engine = None
    sessionmaker = None
    Session = None

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./odeadev_tts.db")
IS_SQLITE = DATABASE_URL.startswith("sqlite")

# Production-grade connection pooling
if create_engine:
    if IS_SQLITE:
        # SQLite: Use NullPool (no connection pooling) to avoid locking issues
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                "check_same_thread": False,
                "timeout": 30.0,  # 30 second timeout for lock wait
            },
            poolclass=NullPool,
            echo=os.getenv("SQL_DEBUG", "false").lower() == "true",
        )
        
        # Enable WAL mode for better concurrency
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
            cursor.execute("PRAGMA busy_timeout=30000")  # 30 second timeout
            cursor.close()
    else:
        # PostgreSQL: Use connection pooling
        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_timeout=30,
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_pre_ping=True,  # Test connections before use
            echo=os.getenv("SQL_DEBUG", "false").lower() == "true",
        )
    
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False  # Don't expire objects after commit
    )
else:
    engine = None
    SessionLocal = None


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions with proper error handling.
    
    Yields:
        Session: SQLAlchemy database session
        
    Ensures:
        - Session is always closed
        - Transactions are committed on success
        - Transactions are rolled back on error
    """
    if SessionLocal is None:
        raise RuntimeError("SQLAlchemy not available in this environment")
    
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        # Re-raise with context
        raise RuntimeError(f"Database error: {type(e).__name__}") from e
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions (for scripts and background tasks).
    
    Usage:
        with get_session() as db:
            user = db.query(User).first()
    """
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


def health_check() -> dict:
    """
    Check database health.
    
    Returns:
        dict: Health status with details
    """
    if SessionLocal is None:
        return {"status": "unavailable", "error": "SQLAlchemy not configured"}
    
    try:
        db = SessionLocal()
        # Simple query to test connection
        db.execute(select(1))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": type(e).__name__}


def update_user_quota_atomic(db: Session, user_id: int, seconds_to_add: float) -> None:
    """
    Atomically update user quota with row-level locking to prevent race conditions.
    
    Args:
        db: Database session
        user_id: User ID
        seconds_to_add: Seconds to add to used_seconds
        
    Raises:
        ValueError: If user not found or insufficient quota
        SQLAlchemyError: On database errors
    """
    from .models import User
    
    # Use SELECT FOR UPDATE to lock the row
    user = db.query(User).filter(User.id == user_id).with_for_update().first()
    
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    if not user.is_active:
        raise ValueError("User account is inactive")
    
    # Check quota AFTER locking
    if user.remaining_seconds < seconds_to_add:
        raise ValueError(
            f"Insufficient quota: {user.remaining_seconds:.1f}s remaining, "
            f"{seconds_to_add:.1f}s requested"
        )
    
    # Update quota
    user.used_seconds += seconds_to_add
    db.flush()  # Flush changes but don't commit yet


__all__ = [
    "engine",
    "SessionLocal",
    "get_db",
    "get_session",
    "health_check",
    "update_user_quota_atomic",
]
