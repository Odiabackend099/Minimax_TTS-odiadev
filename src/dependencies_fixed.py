"""Production-ready FastAPI dependencies with security hardening."""
from __future__ import annotations
import os
import hmac
import time
import random
from typing import Optional
from functools import lru_cache

try:
    from fastapi import Header, HTTPException, Depends, Request
    from sqlalchemy.orm import Session
    from cachetools import TTLCache
except Exception:
    Header = HTTPException = Depends = Session = Request = None
    TTLCache = None

from .database_fixed import get_db
from .models import User, Plan, PLAN_CONFIGS
from .auth import hash_api_key

# Optional auth bypass for testing (set ENFORCE_AUTH=false)
ENFORCE_AUTH = os.getenv("ENFORCE_AUTH", "true").lower() == "true"

# Rate limiting cache (user_id -> list of request timestamps)
_rate_limit_cache = TTLCache(maxsize=10000, ttl=60) if TTLCache else {}


def constant_time_compare(a: str, b: str) -> bool:
    """
    Constant-time string comparison to prevent timing attacks.
    
    Args:
        a: First string
        b: Second string
        
    Returns:
        bool: True if strings are equal
    """
    return hmac.compare_digest(a.encode(), b.encode())


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Authentication dependency with timing attack protection.
    
    Security features:
    - Constant-time comparison
    - Random delay on failure to prevent timing analysis
    - Query optimization to reduce timing variance
    
    Args:
        authorization: Authorization header value
        db: Database session
        
    Returns:
        User: Authenticated user
        
    Raises:
        HTTPException: 401 if authentication fails
    """
    # Testing mode: return a mock user if auth is disabled
    if not ENFORCE_AUTH:
        mock_user = db.query(User).filter(User.is_active == True).first()
        if mock_user:
            return mock_user
        
        # Create test user
        from .auth import generate_api_key, hash_api_key as hash_key
        api_key = generate_api_key()
        mock_user = User(
            name="Test User",
            email="test@example.com",
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
    start_time = time.time()
    
    if not authorization:
        time.sleep(random.uniform(0.1, 0.3))  # Random delay
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header"
        )
    
    if not authorization.startswith("Bearer "):
        time.sleep(random.uniform(0.1, 0.3))
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header format"
        )
    
    api_key = authorization[7:]  # Remove "Bearer " prefix
    
    if not api_key or len(api_key) < 20:
        time.sleep(random.uniform(0.1, 0.3))
        raise HTTPException(
            status_code=401,
            detail="Invalid API key format"
        )
    
    # Hash the provided key
    api_key_hash = hash_api_key(api_key)
    
    # Fetch active users (optimized query)
    users = db.query(User).filter(
        User.is_active == True
    ).all()
    
    # Constant-time comparison to find matching user
    matched_user = None
    for user in users:
        if constant_time_compare(user.api_key_hash, api_key_hash):
            matched_user = user
            # Don't break early - complete the loop for constant time
    
    # Calculate elapsed time
    elapsed = time.time() - start_time
    
    # Ensure minimum response time to prevent timing analysis
    min_time = 0.1
    if elapsed < min_time:
        time.sleep(min_time - elapsed + random.uniform(0, 0.1))
    
    if not matched_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return matched_user


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Admin-only dependency.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Admin user
        
    Raises:
        HTTPException: 403 if user is not admin
    """
    # Enterprise users are admins (extend with is_admin field later)
    if current_user.plan != Plan.ENTERPRISE:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    
    return current_user


async def check_rate_limit(
    request: Request,
    user: User = Depends(get_current_user)
) -> User:
    """
    Rate limiting dependency.
    
    Enforces per-user rate limits based on plan:
    - Free: 10 RPM
    - Basic: 30 RPM
    - Pro: 60 RPM
    - Enterprise: 120 RPM
    
    Args:
        request: FastAPI request
        user: Current user
        
    Returns:
        User: Current user (if rate limit not exceeded)
        
    Raises:
        HTTPException: 429 if rate limit exceeded
    """
    if not ENFORCE_AUTH:
        return user  # Skip rate limiting in test mode
    
    # Get rate limit for user's plan
    rpm_limit = PLAN_CONFIGS[user.plan]["rpm"]
    
    # Get current timestamp
    now = time.time()
    minute_ago = now - 60
    
    # Get or create request log for user
    if user.id not in _rate_limit_cache:
        _rate_limit_cache[user.id] = []
    
    request_times = _rate_limit_cache[user.id]
    
    # Remove requests older than 1 minute
    request_times[:] = [t for t in request_times if t > minute_ago]
    
    # Check if rate limit exceeded
    if len(request_times) >= rpm_limit:
        # Calculate retry-after
        oldest_request = min(request_times)
        retry_after = int(60 - (now - oldest_request) + 1)
        
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. {rpm_limit} requests per minute allowed for {user.plan.value} plan.",
            headers={"Retry-After": str(retry_after)}
        )
    
    # Add current request
    request_times.append(now)
    
    return user


@lru_cache(maxsize=1)
def get_rate_limiter_cache():
    """
    Get rate limiter cache (singleton).
    
    Returns:
        dict or TTLCache: Cache for rate limiting
    """
    return _rate_limit_cache


def clear_rate_limit_cache():
    """Clear rate limit cache (for testing)."""
    _rate_limit_cache.clear()


__all__ = [
    "get_db",
    "get_current_user",
    "get_admin_user",
    "check_rate_limit",
    "clear_rate_limit_cache",
]
