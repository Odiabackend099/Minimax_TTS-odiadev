"""Entry point for the OdeaDev‑AI‑TTS service."""
from __future__ import annotations
import os
from typing import List, Optional

try:
    from fastapi import FastAPI, Depends, HTTPException
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
    
    
    @app.get("/v1/voices", response_model=List[VoiceResponse], tags=["Voices"])
    def list_voices(
        language: Optional[str] = None,
        gender: Optional[str] = None,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
    ):
        """List available voices. Optionally filter by language or gender."""
        query = db.query(Voice).filter(Voice.is_active == True)
        
        if language:
            query = query.filter(Voice.language == language)
        
        if gender:
            query = query.filter(Voice.gender == Gender[gender.upper()])
        
        voices = query.all()
        return [VoiceResponse.model_validate(v) for v in voices]
    
    
    @app.get("/v1/me", response_model=UserResponse, tags=["User"])
    def get_current_user_info(user: User = Depends(get_current_user)):
        """Get current authenticated user's information."""
        return UserResponse.model_validate(user)
    
    
    # ==================== TTS Endpoint ====================
    @app.post("/v1/tts", response_model=TTSResponse, tags=["TTS"])
    def generate_speech(
        request: TTSRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
    ):
        """
        Generate speech from text using verified ODIADEV AI TTS voices.
        
        Available voices:
        - american-female: Professional American female voice
        - american-male: Marcus American male voice (authoritative)
        - nigerian-female: Ezinne Nigerian female voice (professional)
        - nigerian-male: Odia Nigerian male voice (authoritative)
        
        Requires valid API key in Authorization header.
        """
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
        
        # Get voice by friendly name or use default
        voice = None
        if request.voice_name:
            voice = db.query(Voice).filter(
                Voice.friendly_name == request.voice_name,
                Voice.is_active == True
            ).first()
            
            if not voice:
                raise HTTPException(
                    status_code=404,
                    detail=f"Voice '{request.voice_name}' not found. Use GET /v1/voices to list available voices."
                )
        else:
            # Use default voice (first active voice)
            voice = db.query(Voice).filter(Voice.is_active == True).first()
            if not voice:
                raise HTTPException(
                    status_code=500,
                    detail="No voices configured. Please contact administrator."
                )
        
        # Initialize MiniMax client
        minimax = MinimaxClient()
        
        # Create usage log (before API call)
        usage_log = Usage(
            user_id=user.id,
            voice_id=voice.id,
            text_length=len(request.text),
            status=UsageStatus.ERROR,  # Assume error, update on success
            model_used=request.model,
        )
        
        try:
            # Call MiniMax API
            result = minimax.text_to_speech(
                text=request.text,
                voice_id=voice.minimax_voice_id,
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
                voice_used=voice.friendly_name,
                text_length=len(request.text),
                remaining_quota=user.remaining_seconds,
            )
            
        except MinimaxAPIError as e:
            # Log error
            usage_log.error_message = e.message
            db.add(usage_log)
            db.commit()
            
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
            
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


__all__ = ["app"]
