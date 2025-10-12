"""Production-ready async MiniMax T2A API client with circuit breaker."""
from __future__ import annotations
import os
import base64
import re
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

try:
    import httpx
    from tenacity import (
        retry,
        stop_after_attempt,
        wait_exponential,
        retry_if_exception_type,
        before_sleep_log
    )
    import logging
except Exception:
    httpx = None
    retry = None

logger = logging.getLogger(__name__)


class MinimaxAPIError(Exception):
    """Custom exception for MiniMax API errors."""
    def __init__(self, status_code: int, message: str, details: Any = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(f"MiniMax API Error {status_code}: {message}")


class CircuitBreakerOpen(Exception):
    """Exception raised when circuit breaker is open."""
    pass


class CircuitBreaker:
    """
    Simple circuit breaker implementation.
    
    States:
    - CLOSED: Normal operation
    - OPEN: Too many failures, reject requests
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening
            timeout: Seconds to wait before trying again
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
    
    def record_success(self):
        """Record successful request."""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def record_failure(self):
        """Record failed request."""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")
    
    def can_execute(self) -> bool:
        """Check if request can be executed."""
        if self.state == "CLOSED":
            return True
        
        if self.state == "OPEN":
            # Check if timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout:
                    self.state = "HALF_OPEN"
                    logger.info("Circuit breaker entering HALF_OPEN state")
                    return True
            return False
        
        # HALF_OPEN state - allow one request
        return True


class MinimaxClient:
    """Async client for MiniMax Text-to-Audio API with production hardening."""
    
    ALLOWED_BASE_URLS = [
        "https://api.minimaxi.chat",
        "https://api-test.minimaxi.chat",
    ]
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        group_id: Optional[str] = None,
        timeout: int = 10,
        max_retries: int = 3
    ):
        """
        Initialize MiniMax client.
        
        Args:
            api_key: MiniMax API key (JWT token)
            group_id: MiniMax Group ID
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            
        Raises:
            ValueError: If credentials are invalid
        """
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID")
        self.base_url = os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.chat")
        
        # Validation
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY not provided")
        if not self.group_id:
            raise ValueError("MINIMAX_GROUP_ID not provided")
        
        # Validate base URL
        if self.base_url not in self.ALLOWED_BASE_URLS:
            raise ValueError(f"Invalid base URL. Allowed: {self.ALLOWED_BASE_URLS}")
        
        # Validate Group ID format (numeric)
        if not re.match(r'^\d+$', self.group_id):
            raise ValueError("Invalid Group ID format (must be numeric)")
        
        # Validate API key format (JWT-like)
        if not self.api_key.startswith("eyJ"):
            logger.warning("API key doesn't look like a JWT token")
        
        # Create async HTTP client
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, connect=5.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            follow_redirects=False,  # Security: don't follow redirects
        )
        
        self.max_retries = max_retries
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    def _sanitize_text(self, text: str) -> str:
        """
        Sanitize text input to prevent injection attacks.
        
        Args:
            text: Input text
            
        Returns:
            str: Sanitized text
        """
        # Remove control characters
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long
        max_length = 5000
        if len(text) > max_length:
            text = text[:max_length]
            logger.warning(f"Text truncated to {max_length} characters")
        
        return text.strip()
    
    def _validate_parameters(self, voice_id: str, model: str, speed: float, pitch: int):
        """
        Validate TTS parameters.
        
        Args:
            voice_id: Voice ID
            model: Model name
            speed: Speech speed
            pitch: Voice pitch
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not voice_id:
            raise ValueError("voice_id is required")
        
        if speed < 0.5 or speed > 2.0:
            raise ValueError("speed must be between 0.5 and 2.0")
        
        if pitch < -12 or pitch > 12:
            raise ValueError("pitch must be between -12 and 12")
        
        # Validate model format
        if not re.match(r'^speech-0[12]-(hd|turbo)', model):
            raise ValueError(f"Invalid model format: {model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        before_sleep=before_sleep_log(logger, logging.WARNING) if logger else None
    )
    async def text_to_speech(
        self,
        text: str,
        voice_id: str,
        model: str = "speech-02-turbo",
        speed: float = 1.0,
        pitch: int = 0,
        emotion: str = "neutral",
    ) -> Dict[str, Any]:
        """
        Convert text to speech using MiniMax API (async with retries).
        
        Args:
            text: Text to convert to speech
            voice_id: MiniMax voice ID
            model: Model to use
            speed: Speech speed (0.5-2.0)
            pitch: Voice pitch (-12 to 12)
            emotion: Emotion
            
        Returns:
            dict with keys:
                - audio_data: bytes of MP3 audio
                - audio_base64: base64-encoded audio
                - duration_seconds: estimated duration
                - sample_rate: audio sample rate
                
        Raises:
            MinimaxAPIError: If API request fails
            CircuitBreakerOpen: If circuit breaker is open
        """
        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            raise CircuitBreakerOpen("Circuit breaker is OPEN - too many recent failures")
        
        # Sanitize and validate inputs
        text = self._sanitize_text(text)
        self._validate_parameters(voice_id, model, speed, pitch)
        
        # Build URL
        url = f"{self.base_url}/v1/t2a_v2?GroupId={self.group_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "OdeaDev-AI-TTS/1.0",
        }
        
        payload = {
            "text": text,
            "model": model,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "pitch": pitch,
                "emotion": emotion,
            },
        }
        
        try:
            logger.info(f"Calling MiniMax API: {len(text)} chars, voice={voice_id}, model={model}")
            
            response = await self.client.post(url, headers=headers, json=payload)
            
            # Check HTTP status
            if response.status_code != 200:
                error_detail = response.text[:200] if response.text else "No details"
                self.circuit_breaker.record_failure()
                raise MinimaxAPIError(
                    response.status_code,
                    f"HTTP {response.status_code}",
                    error_detail
                )
            
            data = response.json()
            
            # Check MiniMax API response status
            base_resp = data.get("base_resp", {})
            status_code = base_resp.get("status_code")
            status_msg = base_resp.get("status_msg", "Unknown error")
            
            if status_code != 0:
                self.circuit_breaker.record_failure()
                
                # Map MiniMax error codes to readable messages
                error_messages = {
                    1008: "Insufficient balance in MiniMax account. Please add credits.",
                    2013: "Invalid parameters provided to MiniMax API.",
                    401: "Invalid MiniMax API key or authentication failed.",
                    403: "Access forbidden. Check API key permissions.",
                    429: "MiniMax API rate limit exceeded.",
                }
                
                readable_msg = error_messages.get(status_code, status_msg)
                raise MinimaxAPIError(status_code, readable_msg, data)
            
            # Extract audio data
            audio_hex = data.get("data", {}).get("audio")
            if not audio_hex:
                self.circuit_breaker.record_failure()
                raise MinimaxAPIError(500, "No audio data in response", data)
            
            # Decode hex to bytes
            try:
                audio_bytes = bytes.fromhex(audio_hex)
            except ValueError as e:
                self.circuit_breaker.record_failure()
                raise MinimaxAPIError(500, f"Invalid audio hex format: {e}", audio_hex[:100])
            
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            
            # Estimate duration (rough estimate: ~150 words per minute)
            word_count = len(text.split())
            estimated_duration = (word_count / 150) * 60 / speed
            
            # Record success
            self.circuit_breaker.record_success()
            
            logger.info(f"MiniMax API success: {len(audio_bytes)} bytes, ~{estimated_duration:.1f}s")
            
            return {
                "audio_data": audio_bytes,
                "audio_base64": audio_base64,
                "duration_seconds": estimated_duration,
                "sample_rate": 32000,  # Default MiniMax sample rate
            }
            
        except httpx.TimeoutException:
            self.circuit_breaker.record_failure()
            logger.error("MiniMax API timeout")
            raise MinimaxAPIError(408, "Request to MiniMax API timed out")
        
        except httpx.NetworkError as e:
            self.circuit_breaker.record_failure()
            logger.error(f"MiniMax API network error: {e}")
            raise MinimaxAPIError(503, "Could not connect to MiniMax API")
        
        except httpx.HTTPStatusError as e:
            self.circuit_breaker.record_failure()
            logger.error(f"MiniMax API HTTP error: {e}")
            raise MinimaxAPIError(e.response.status_code, f"HTTP error: {e}")
        
        except (ValueError, KeyError) as e:
            self.circuit_breaker.record_failure()
            logger.error(f"MiniMax API parse error: {e}")
            raise MinimaxAPIError(500, f"Failed to parse MiniMax response: {e}")


# Singleton client instance (for connection pooling)
_client_instance: Optional[MinimaxClient] = None


async def get_minimax_client() -> MinimaxClient:
    """
    Get or create singleton MiniMax client.
    
    Returns:
        MinimaxClient: Shared client instance
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = MinimaxClient()
    return _client_instance


async def close_minimax_client():
    """Close singleton client."""
    global _client_instance
    if _client_instance:
        await _client_instance.close()
        _client_instance = None


__all__ = [
    "MinimaxClient",
    "MinimaxAPIError",
    "CircuitBreakerOpen",
    "get_minimax_client",
    "close_minimax_client",
]
