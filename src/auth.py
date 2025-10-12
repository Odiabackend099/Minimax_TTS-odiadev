"""Authentication and API key utilities."""
from __future__ import annotations
import secrets, hashlib

API_KEY_BYTES = 32

def generate_api_key() -> str:
    return secrets.token_urlsafe(API_KEY_BYTES)

def hash_api_key(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def verify_api_key(key: str, hashed: str) -> bool:
    return hash_api_key(key) == hashed
