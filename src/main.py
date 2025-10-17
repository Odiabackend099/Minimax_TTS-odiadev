"""Entry point for the ODIADEV AI TTS service."""
from __future__ import annotations
import os
import json
import uuid
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    from fastapi import FastAPI, Depends, HTTPException, Request
    from sqlalchemy.orm import Session
    from dotenv import load_dotenv
except Exception:
    FastAPI = Depends = HTTPException = Session = None
    load_dotenv = lambda: None

# Load environment variables
load_dotenv()

from .database import get_session
from .models import User, Voice, Usage, Plan, Gender, UsageStatus, PLAN_CONFIGS
from .schemas import (
    HealthResponse, UserCreate, UserCreateResponse, UserResponse,
    QuotaUpdate, VoiceCreate, VoiceResponse, TTSRequest, TTSResponse
)
from .auth import generate_api_key, hash_api_key
from .dependencies import get_db, get_current_user, get_admin_user
from .minimax_client import MinimaxClient, MinimaxAPIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load voices configuration
VOICES_CONFIG = {}
try:
    with open("voices.json", "r") as f:
        VOICES_CONFIG = json.load(f)
except FileNotFoundError:
    logger.warning("voices.json not found, using default voices")
    VOICES_CONFIG = {
        "voices": [
            {"id": "marcus", "name": "Marcus", "minimax_voice_id": "moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc"},
            {"id": "marcy", "name": "Marcy", "minimax_voice_id": "moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a"},
            {"id": "austyn", "name": "Austyn", "minimax_voice_id": "moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc"},
            {"id": "joslyn", "name": "Joslyn", "minimax_voice_id": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82"}
        ]
    }

def generate_silent_audio(duration_seconds: float) -> str:
    """Generate silent audio as base64 string for fallback."""
    import base64
    import io
    import wave
    
    # Create silent audio data
    sample_rate = 32000
    num_samples = int(sample_rate * duration_seconds)
    silent_data = b'\x00' * (num_samples * 2)  # 16-bit audio
    
    # Create WAV file in memory
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(silent_data)
    
    # Convert to base64
    wav_buffer.seek(0)
    return base64.b64encode(wav_buffer.read()).decode('utf-8')

# Initialize FastAPI app
app = FastAPI(
    title="ODIADEV AI TTS",
    version="1.0.0",
    description="Production-ready TTS service with verified voice characteristics, authentication, quotas, and billing"
) if FastAPI else None

if app:
    # ==================== Health Check ====================
    @app.get("/health", response_model=HealthResponse, tags=["Health"])
    def health():
        """Health check endpoint."""
        return {"status": "ok"}
    
    
    # ==================== Admin Endpoints ====================
    @app.post("/admin/users", response_model=UserCreateResponse, tags=["Admin"], status_code=201)
    def create_user(
        user_data: UserCreate,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
    ):
        """
        Create a new user with API key.
        
        **Admin only** - Returns the plain API key once. Store it securely!
        """
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Generate API key
        api_key = generate_api_key()
        api_key_hash = hash_api_key(api_key)
        
        # Get plan configuration
        plan_enum = Plan[user_data.plan.upper()]
        plan_config = PLAN_CONFIGS[plan_enum]
        
        # Create user
        user = User(
            name=user_data.name,
            email=user_data.email,
            api_key_hash=api_key_hash,
            plan=plan_enum,
            quota_seconds=plan_config["quota_seconds"],
            used_seconds=0.0,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return UserCreateResponse(
            user=UserResponse.model_validate(user),
            api_key=api_key  # Plain key shown only once!
        )
    
    
    @app.get("/admin/users/{user_id}", response_model=UserResponse, tags=["Admin"])
    def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
    ):
        """Get user details by ID. **Admin only**"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse.model_validate(user)
    
    
    @app.put("/admin/users/{user_id}/quota", response_model=UserResponse, tags=["Admin"])
    def update_user_quota(
        user_id: int,
        quota_update: QuotaUpdate,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
    ):
        """Update user quota or reset usage. **Admin only**"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if quota_update.quota_seconds is not None:
            user.quota_seconds = quota_update.quota_seconds
        
        if quota_update.used_seconds is not None:
            user.used_seconds = quota_update.used_seconds
        
        db.commit()
        db.refresh(user)
        
        return UserResponse.model_validate(user)
    
    
    @app.post("/admin/voices", response_model=VoiceResponse, tags=["Admin"], status_code=201)
    def create_voice(
        voice_data: VoiceCreate,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
    ):
        """Register a new voice. **Admin only**"""
        # Check if friendly name already exists
        existing = db.query(Voice).filter(Voice.friendly_name == voice_data.friendly_name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Voice name already exists")
        
        voice = Voice(
            friendly_name=voice_data.friendly_name,
            minimax_voice_id=voice_data.minimax_voice_id,
            language=voice_data.language,
            gender=Gender[voice_data.gender.upper()],
            description=voice_data.description,
            is_cloned=voice_data.is_cloned,
        )
        
        db.add(voice)
        db.commit()
        db.refresh(voice)
        
        return VoiceResponse.model_validate(voice)
    
    
    @app.get("/v1/voices/list", response_model=List[Dict[str, Any]], tags=["Voices"])
    def list_voices(
        language: Optional[str] = None,
        gender: Optional[str] = None
    ):
        """List available voices. Optionally filter by language or gender."""
        voices = VOICES_CONFIG["voices"]
        
        # Filter by language if specified
        if language:
            voices = [v for v in voices if v.get("language", "").startswith(language)]
        
        # Filter by gender if specified
        if gender:
            voices = [v for v in voices if v.get("gender", "").lower() == gender.lower()]
        
        # Return only active voices
        active_voices = [v for v in voices if v.get("is_active", True)]
        
        # Format response
        response = []
        for voice in active_voices:
            response.append({
                "id": voice["id"],
                "name": voice["name"],
                "description": voice.get("description", ""),
                "language": voice.get("language", "en-US"),
                "gender": voice.get("gender", "unknown"),
                "accent": voice.get("accent", "unknown"),
                "tone": voice.get("tone", "neutral"),
                "use_cases": voice.get("use_cases", []),
                "is_verified": voice.get("is_verified", False)
            })
        
        return response
    
    
    @app.get("/v1/me", response_model=UserResponse, tags=["User"])
    def get_current_user_info(user: User = Depends(get_current_user)):
        """Get current authenticated user's information."""
        return UserResponse.model_validate(user)
    
    
    # ==================== TTS Endpoint ====================
    @app.post("/v1/tts", response_model=TTSResponse, tags=["TTS"])
    def generate_speech(
        request: TTSRequest,
        http_request: Request,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
    ):
        """
        Generate speech from text using verified ODIADEV AI TTS voices.
        
        Available voices:
        - marcus: American Male - Professional, authoritative tone
        - marcy: American Female - Clear, professional tone
        - austyn: African Male - Strong, confident tone
        - joslyn: African Female - Warm, professional tone
        
        Requires valid API key in Authorization header.
        """
        # Generate request ID for logging
        request_id = str(uuid.uuid4())[:8]
        
        # Validate voice_id
        valid_voice_ids = [voice["id"] for voice in VOICES_CONFIG["voices"]]
        if request.voice_name and request.voice_name not in valid_voice_ids:
            logger.error(f"Request {request_id}: Invalid voice_id '{request.voice_name}'")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid voice_id '{request.voice_name}'. Valid options: {', '.join(valid_voice_ids)}"
            )
        
        # Validate text length
        max_length = int(os.getenv("MAX_TEXT_LENGTH", "5000"))
        if len(request.text) > max_length:
            logger.error(f"Request {request_id}: Text too long ({len(request.text)} chars)")
            raise HTTPException(
                status_code=400,
                detail=f"Text too long. Maximum {max_length} characters allowed."
            )
        
        # Log request (without full text for privacy)
        text_snippet = request.text[:50] + "..." if len(request.text) > 50 else request.text
        logger.info(f"Request {request_id}: TTS request for voice '{request.voice_name}', text: '{text_snippet}'")
        # Check if user has remaining quota
        if user.remaining_seconds <= 0:
            raise HTTPException(
                status_code=429,
                detail=f"Quota exceeded. Used {user.used_seconds:.1f}/{user.quota_seconds:.1f} seconds. "
                       f"Upgrade your plan or wait for quota reset."
            )
        
        # Estimate audio duration (conservative estimate)
        word_count = len(request.text.split())
        estimated_seconds = (word_count / 150) * 60 / request.speed
        
        # Check if estimated duration exceeds remaining quota
        if estimated_seconds > user.remaining_seconds:
            raise HTTPException(
                status_code=429,
                detail=f"Estimated audio duration ({estimated_seconds:.1f}s) exceeds remaining quota "
                       f"({user.remaining_seconds:.1f}s)."
            )
        
        # Get voice by ID or use default
        voice_config = None
        if request.voice_name:
            voice_config = next((v for v in VOICES_CONFIG["voices"] if v["id"] == request.voice_name), None)
            
            if not voice_config:
                raise HTTPException(
                    status_code=404,
                    detail=f"Voice '{request.voice_name}' not found. Use GET /v1/voices/list to list available voices."
                )
        else:
            # Use default voice (first active voice)
            voice_config = next((v for v in VOICES_CONFIG["voices"] if v.get("is_active", True)), None)
            if not voice_config:
                raise HTTPException(
                    status_code=500,
                    detail="No voices configured. Please contact administrator."
                )
        
        # Initialize MiniMax client
        minimax = MinimaxClient()
        
        # Create usage log (before API call)
        usage_log = Usage(
            user_id=user.id,
            voice_id=0,  # No database voice ID for config-based voices
            text_length=len(request.text),
            status=UsageStatus.ERROR,  # Assume error, update on success
            model_used=request.model,
        )
        
        try:
            # Call MiniMax API
            result = minimax.text_to_speech(
                text=request.text,
                voice_id=voice_config["minimax_voice_id"],
                model=request.model,
                speed=request.speed,
                pitch=request.pitch,
                emotion=request.emotion,
            )
            
            # Update usage log with success
            usage_log.audio_seconds = result["duration_seconds"]
            usage_log.status = UsageStatus.SUCCESS
            
            # Update user's used seconds
            user.used_seconds += result["duration_seconds"]
            
            # Save to database
            db.add(usage_log)
            db.commit()
            db.refresh(user)
            
            return TTSResponse(
                audio_base64=result["audio_base64"],
                duration_seconds=result["duration_seconds"],
                sample_rate=result["sample_rate"],
                voice_used=voice_config["id"],
                text_length=len(request.text),
                remaining_quota=user.remaining_seconds,
            )
            
        except MinimaxAPIError as e:
            # Log error
            usage_log.error_message = e.message
            db.add(usage_log)
            db.commit()
            
            logger.error(f"Request {request_id}: MiniMax API error - {e.message}")
            
            # Check if we should return silent audio instead of error
            fallback_to_silent = os.getenv("FALLBACK_TO_SILENT_AUDIO", "true").lower() == "true"
            
            if fallback_to_silent:
                logger.warning(f"Request {request_id}: Returning silent audio due to TTS failure")
                # Generate 1-second silent audio
                silent_audio = generate_silent_audio(1.0)
                return TTSResponse(
                    audio_base64=silent_audio,
                    duration_seconds=1.0,
                    sample_rate=32000,
                    voice_used=request.voice_name or "unknown",
                    text_length=len(request.text),
                    remaining_quota=user.remaining_seconds,
                )
            else:
                # Return appropriate HTTP error
                if e.status_code == 1008:
                    raise HTTPException(status_code=503, detail=e.message)
                elif e.status_code in [401, 403]:
                    raise HTTPException(status_code=500, detail="Service authentication error. Contact administrator.")
                else:
                    raise HTTPException(status_code=500, detail=f"TTS generation failed: {e.message}")
        
        except Exception as e:
            # Log unexpected errors
            usage_log.error_message = str(e)
            db.add(usage_log)
            db.commit()
            
            logger.error(f"Request {request_id}: Unexpected error - {str(e)}")
            
            # Check if we should return silent audio instead of error
            fallback_to_silent = os.getenv("FALLBACK_TO_SILENT_AUDIO", "true").lower() == "true"
            
            if fallback_to_silent:
                logger.warning(f"Request {request_id}: Returning silent audio due to unexpected error")
                # Generate 1-second silent audio
                silent_audio = generate_silent_audio(1.0)
                return TTSResponse(
                    audio_base64=silent_audio,
                    duration_seconds=1.0,
                    sample_rate=32000,
                    voice_used=request.voice_name or "unknown",
                    text_length=len(request.text),
                    remaining_quota=user.remaining_seconds,
                )
            else:
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


__all__ = ["app"]
