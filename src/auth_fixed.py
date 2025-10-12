"""Production-ready authentication with stronger key generation."""
from __future__ import annotations
import secrets
import hashlib
import re
from datetime import datetime
from typing import Tuple

# Use 512-bit keys for quantum resistance
API_KEY_BYTES = 64
API_KEY_VERSION = "v1"


def generate_api_key() -> str:
    """
    Generate cryptographically secure API key.
    
    Returns:
        str: URL-safe API key (512 bits of entropy)
        
    Format: v1_<timestamp>_<random_token>
    Example: v1_2025-01-12T02:30:00_xK3mP9vL5tQ1wY7hJ6cB4aD0sZ8eU2oK5gM3iN6pW9rT1...
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_token = secrets.token_urlsafe(API_KEY_BYTES)
    
    # Format: version_timestamp_token
    api_key = f"{API_KEY_VERSION}_{timestamp}_{random_token}"
    
    return api_key


def hash_api_key(key: str) -> str:
    """
    Hash API key using SHA-256.
    
    Note: For production, consider using Argon2 or bcrypt for password-like
    storage, but SHA-256 is acceptable for API keys with high entropy.
    
    Args:
        key: Plain API key
        
    Returns:
        str: Hexadecimal hash (64 characters)
    """
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def verify_api_key(key: str, hashed: str) -> bool:
    """
    Verify API key using constant-time comparison.
    
    Args:
        key: Plain API key to verify
        hashed: Stored hash
        
    Returns:
        bool: True if key matches hash
    """
    import hmac
    computed_hash = hash_api_key(key)
    return hmac.compare_digest(computed_hash, hashed)


def validate_api_key_format(key: str) -> Tuple[bool, str]:
    """
    Validate API key format before attempting authentication.
    
    Args:
        key: API key to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not key:
        return False, "API key is empty"
    
    if len(key) < 50:
        return False, "API key too short"
    
    if len(key) > 200:
        return False, "API key too long"
    
    # Check for version prefix
    if not key.startswith(f"{API_KEY_VERSION}_"):
        # Allow legacy keys without version for backward compatibility
        # Remove this check after migration period
        if not re.match(r'^[A-Za-z0-9_-]+$', key):
            return False, "API key contains invalid characters"
        return True, ""
    
    # Validate versioned key format
    parts = key.split("_", 2)
    if len(parts) != 3:
        return False, "Invalid API key format"
    
    version, timestamp, token = parts
    
    if version != API_KEY_VERSION:
        return False, f"Unsupported API key version: {version}"
    
    if not re.match(r'^\d{14}$', timestamp):
        return False, "Invalid timestamp format"
    
    if not re.match(r'^[A-Za-z0-9_-]+$', token):
        return False, "Invalid token format"
    
    return True, ""


def generate_api_key_with_salt() -> Tuple[str, str]:
    """
    Generate API key with additional salt for enhanced security.
    
    Returns:
        Tuple[str, str]: (api_key, salt)
    """
    api_key = generate_api_key()
    salt = secrets.token_hex(16)  # 128-bit salt
    return api_key, salt


def hash_api_key_with_salt(key: str, salt: str) -> str:
    """
    Hash API key with salt using PBKDF2.
    
    Args:
        key: Plain API key
        salt: Salt (hex string)
        
    Returns:
        str: Hashed key with salt prepended
    """
    salt_bytes = bytes.fromhex(salt)
    key_bytes = key.encode("utf-8")
    
    # Use PBKDF2 with 100,000 iterations (OWASP recommendation)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        key_bytes,
        salt_bytes,
        iterations=100_000,
        dklen=32
    )
    
    # Return salt:hash format
    return f"{salt}:{hashed.hex()}"


def verify_api_key_with_salt(key: str, stored_hash: str) -> bool:
    """
    Verify API key hashed with salt.
    
    Args:
        key: Plain API key
        stored_hash: Stored hash in format "salt:hash"
        
    Returns:
        bool: True if key matches
    """
    import hmac
    
    try:
        salt, expected_hash = stored_hash.split(":", 1)
    except ValueError:
        return False
    
    computed_hash = hash_api_key_with_salt(key, salt)
    _, computed_hash_only = computed_hash.split(":", 1)
    
    return hmac.compare_digest(computed_hash_only, expected_hash)


def rotate_api_key(old_key: str) -> str:
    """
    Rotate API key (generate new key, marking old as deprecated).
    
    Args:
        old_key: Current API key
        
    Returns:
        str: New API key
        
    Note: Update database to mark old key as deprecated with expiry date
    """
    return generate_api_key()


def is_api_key_expired(key: str, max_age_days: int = 365) -> bool:
    """
    Check if API key has expired based on timestamp.
    
    Args:
        key: API key
        max_age_days: Maximum age in days
        
    Returns:
        bool: True if key is expired
    """
    if not key.startswith(f"{API_KEY_VERSION}_"):
        # Legacy keys don't have timestamps - consider them never expired
        return False
    
    parts = key.split("_", 2)
    if len(parts) != 3:
        return False
    
    _, timestamp_str, _ = parts
    
    try:
        key_date = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
        age_days = (datetime.utcnow() - key_date).days
        return age_days > max_age_days
    except ValueError:
        return False


__all__ = [
    "generate_api_key",
    "hash_api_key",
    "verify_api_key",
    "validate_api_key_format",
    "generate_api_key_with_salt",
    "hash_api_key_with_salt",
    "verify_api_key_with_salt",
    "rotate_api_key",
    "is_api_key_expired",
]
