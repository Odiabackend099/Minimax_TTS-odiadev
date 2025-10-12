"""FastAPI dependencies for authentication and authorization."""
from __future__ import annotations
import os
from typing import Optional

try:
    from fastapi import Header, HTTPException, Depends
    from sqlalchemy.orm import Session
except Exception:
    Header = HTTPException = Depends = Session = None

from .database import SessionLocal
from .models import User
from .auth import hash_api_key

# Optional auth bypass for testing (set ENFORCE_AUTH=false)
ENFORCE_AUTH = os.getenv("ENFORCE_AUTH", "true").lower() == "true"


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Authentication dependency that validates API key from Authorization header.
    
    Expected format: Authorization: Bearer <api_key>
    
    Can be bypassed when ENFORCE_AUTH=false (for testing only).
    
    Raises:
        HTTPException: 401 if key is invalid or missing
    """
    # Testing mode: return a mock user if auth is disabled
    if not ENFORCE_AUTH:
        # Return first active user or create a mock one
        mock_user = db.query(User).filter(User.is_active == True).first()
        if mock_user:
            return mock_user
        # If no users exist, create a test user
        from .models import Plan, PLAN_CONFIGS
        from .auth import generate_api_key, hash_api_key as hash_key
        api_key = generate_api_key()
        mock_user = User(
            name="Test User",
            email="test@render.com",
            api_key_hash=hash_key(api_key),
            plan=Plan.ENTERPRISE,
            quota_seconds=PLAN_CONFIGS[Plan.ENTERPRISE]["quota_seconds"],
            used_seconds=0.0,
            is_active=True,
        )
        db.add(mock_user)
        db.commit()
        db.refresh(mock_user)
        return mock_user
    
    # Production mode: enforce authentication
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header format. Expected: Bearer <api_key>"
        )
    
    api_key = authorization[7:]  # Remove "Bearer " prefix
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is empty"
        )
    
    # Hash the provided key and look up in database
    api_key_hash = hash_api_key(api_key)
    user = db.query(User).filter(User.api_key_hash == api_key_hash).first()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )
    
    return user


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Admin-only dependency that checks if user has admin privileges.
    
    For now, we'll use a simple check (can be expanded later).
    In production, add an `is_admin` field to User model.
    
    Raises:
        HTTPException: 403 if user is not admin
    """
    # TODO: Add is_admin field to User model
    # For now, enterprise users are considered admins
    if current_user.plan.value != "enterprise":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    
    return current_user
